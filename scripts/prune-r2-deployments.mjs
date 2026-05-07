import { execFileSync } from "node:child_process";

const bucket = process.env.R2_BUCKET || "leadership-legacy";
const keep = Number(process.env.R2_KEEP_DEPLOYMENTS || 3);
const prefix = "deployments/";

function wrangler(args, opts = {}) {
  return execFileSync("npx", ["wrangler", ...args], {
    encoding: opts.encoding || "utf8",
    stdio: opts.stdio || ["ignore", "pipe", "pipe"]
  });
}

function listObjects() {
  const raw = wrangler(["r2", "object", "list", bucket, "--prefix", prefix, "--remote", "--json"]);
  return JSON.parse(raw);
}

function deploymentNameFromKey(key) {
  const rest = key.slice(prefix.length);
  const first = rest.split("/")[0];
  if (!first || first.startsWith("_")) return null;
  return first;
}

const objects = listObjects();
const deploymentMap = new Map();

for (const object of objects) {
  const deployment = deploymentNameFromKey(object.key);
  if (!deployment) continue;

  const current = deploymentMap.get(deployment) || {
    deployment,
    uploaded: object.uploaded || object.created || "",
    keys: []
  };

  current.keys.push(object.key);

  const objectTime = object.uploaded || object.created || "";
  if (objectTime && (!current.uploaded || objectTime > current.uploaded)) {
    current.uploaded = objectTime;
  }

  deploymentMap.set(deployment, current);
}

const deployments = [...deploymentMap.values()]
  .sort((a, b) => String(b.uploaded).localeCompare(String(a.uploaded)));

const toKeep = deployments.slice(0, keep);
const toDelete = deployments.slice(keep);

console.log(`R2 prune bucket=${bucket} keep=${keep}`);
console.log(`Keeping: ${toKeep.map((item) => item.deployment).join(", ") || "(none)"}`);
console.log(`Deleting: ${toDelete.map((item) => item.deployment).join(", ") || "(none)"}`);

for (const deployment of toDelete) {
  for (const key of deployment.keys) {
    console.log(`R2 delete r2://${bucket}/${key}`);
    execFileSync(
      "npx",
      ["wrangler", "r2", "object", "delete", `${bucket}/${key}`, "--remote"],
      { stdio: "inherit" }
    );
  }
}

console.log("R2 deployment prune complete.");
