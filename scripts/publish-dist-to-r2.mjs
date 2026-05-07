import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";

const bucket = process.env.R2_BUCKET || "leadership-legacy";
const distDir = process.env.DIST_DIR || "dist";
const sha =
  process.env.GITHUB_SHA ||
  execFileSync("git", ["rev-parse", "--short", "HEAD"], { encoding: "utf8" }).trim();

const deploymentKey = `deployments/${sha}`;
const liveKey = "live";
const now = new Date().toISOString();

if (!existsSync(distDir)) {
  console.error(`Missing ${distDir}/. Run npm run build first.`);
  process.exit(1);
}

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const stat = statSync(full);
    if (stat.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

function putObject(localFile, key) {
  console.log(`R2 put ${localFile} -> r2://${bucket}/${key}`);
  execFileSync(
    "npx",
    ["wrangler", "r2", "object", "put", `${bucket}/${key}`, "--file", localFile, "--remote"],
    { stdio: "inherit" }
  );
}

const files = walk(distDir);
const manifest = {
  app: "leadership-legacy",
  sha,
  created_at: now,
  bucket,
  deployment_prefix: deploymentKey,
  live_prefix: liveKey,
  files: files.map((file) => relative(distDir, file).replaceAll("\\", "/"))
};

writeFileSync(".r2-deployment-manifest.json", JSON.stringify(manifest, null, 2) + "\n");

for (const file of files) {
  const rel = relative(distDir, file).replaceAll("\\", "/");
  putObject(file, `${deploymentKey}/${rel}`);
  putObject(file, `${liveKey}/${rel}`);
}

putObject(".r2-deployment-manifest.json", `${deploymentKey}/manifest.json`);
putObject(".r2-deployment-manifest.json", `${liveKey}/manifest.json`);
putObject(".r2-deployment-manifest.json", `deployments/_latest.json`);

console.log(`Published dist to r2://${bucket}/${deploymentKey}/ and r2://${bucket}/${liveKey}/`);
