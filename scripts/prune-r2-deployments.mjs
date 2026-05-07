import { execFileSync } from "node:child_process";

const bucket = process.env.R2_BUCKET || "leadership-legacy";
const keep = Number(process.env.R2_KEEP_DEPLOYMENTS || 3);
const liveBaseUrl =
  process.env.LIVE_WORKER_URL ||
  process.env.PLAYWRIGHT_BASE_URL ||
  "https://leadership-legacy.meauxbility.workers.dev";

const deploymentsPrefix = "deployments/";

function run(cmd, args, options = {}) {
  return execFileSync(cmd, args, {
    encoding: options.encoding || "utf8",
    stdio: options.stdio || ["ignore", "pipe", "pipe"]
  });
}

async function fetchJson(url) {
  const response = await fetch(url);
  const text = await response.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`Expected JSON from ${url}, got: ${text.slice(0, 500)}`);
  }

  if (!response.ok || !data.ok) {
    throw new Error(`Request failed for ${url}: ${JSON.stringify(data).slice(0, 500)}`);
  }

  return data;
}

async function listObjectsViaWorker(prefix) {
  const objects = [];
  let cursor = "";

  while (true) {
    const url = new URL("/api/r2/list", liveBaseUrl);
    url.searchParams.set("prefix", prefix);
    url.searchParams.set("limit", "1000");
    if (cursor) url.searchParams.set("cursor", cursor);

    const data = await fetchJson(url.toString());
    objects.push(...(data.objects || []));

    if (!data.truncated || !data.cursor) break;
    cursor = data.cursor;
  }

  return objects;
}

function deploymentNameFromKey(key) {
  if (!key.startsWith(deploymentsPrefix)) return null;

  const rest = key.slice(deploymentsPrefix.length);
  const first = rest.split("/")[0];

  if (!first) return null;
  if (first.startsWith("_")) return null;

  return first;
}

function deleteObject(key) {
  console.log(`R2 delete r2://${bucket}/${key}`);
  execFileSync(
    "npx",
    ["wrangler", "r2", "object", "delete", `${bucket}/${key}`, "--remote"],
    { stdio: "inherit" }
  );
}

console.log(`R2 prune using Worker API: ${liveBaseUrl}/api/r2/list`);
console.log(`Bucket: ${bucket}`);
console.log(`Keep latest deployments: ${keep}`);

const objects = await listObjectsViaWorker(deploymentsPrefix);
const deploymentMap = new Map();

for (const object of objects) {
  const deployment = deploymentNameFromKey(object.key);
  if (!deployment) continue;

  const current = deploymentMap.get(deployment) || {
    deployment,
    uploaded: object.uploaded || "",
    keys: []
  };

  current.keys.push(object.key);

  if (object.uploaded && (!current.uploaded || object.uploaded > current.uploaded)) {
    current.uploaded = object.uploaded;
  }

  deploymentMap.set(deployment, current);
}

const deployments = [...deploymentMap.values()]
  .sort((a, b) => String(b.uploaded).localeCompare(String(a.uploaded)));

const toKeep = deployments.slice(0, keep);
const toDelete = deployments.slice(keep);

console.log(`Found deployments: ${deployments.map((item) => item.deployment).join(", ") || "(none)"}`);
console.log(`Keeping: ${toKeep.map((item) => item.deployment).join(", ") || "(none)"}`);
console.log(`Deleting: ${toDelete.map((item) => item.deployment).join(", ") || "(none)"}`);

for (const deployment of toDelete) {
  for (const key of deployment.keys) {
    deleteObject(key);
  }
}

console.log("R2 deployment prune complete.");
