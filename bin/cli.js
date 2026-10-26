#!/usr/bin/env node

/**
 * expected-2-unexpected CLI entrypoint.
 * Zero-dependency executable running under Bun or Node.js.
 */

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = resolve(__dirname, "..");

const BANNER = `
\x1b[36m╔════════════════════════════════════════════════════════════════════╗
║                expected-2-unexpected CLI v1.0.0                    ║
║      Behavioral Guidelines to Eliminate LLM Coding Mistakes        ║
╚════════════════════════════════════════════════════════════════════╝\x1b[0m
`;

function printHelp() {
  console.log(BANNER);
  console.log(`Usage:
  npx expected-2-unexpected <command> [options]
  bun x expected-2-unexpected <command> [options]

Commands:
  audit [options]     Analyze git diff for surgical containment & sprawl
  check               Run skill package self-test and integrity checks
  install             Install skill to Claude Code, Antigravity, and Codex
  guidelines          Display the 4 core pillars and simplicity ladder
  version             Print version
  help                Show this message

Audit Options:
  --staged            Analyze staged git changes
  --base <ref>        Compare against base commit or branch (e.g. main)
  --file <path>       Analyze a saved .diff file
  --json              Output raw JSON report

Examples:
  npx expected-2-unexpected audit --staged
  npx expected-2-unexpected audit --base main
  npx expected-2-unexpected check
  npx expected-2-unexpected install
`);
}

function runAudit(args) {
  const pythonScript = join(ROOT_DIR, "skills", "expected-2-unexpected", "scripts", "verify_surgical_diff.py");
  const fallbackScript = join(ROOT_DIR, "scripts", "verify_surgical_diff.py");
  const scriptToRun = existsSync(pythonScript) ? pythonScript : fallbackScript;

  if (!existsSync(scriptToRun)) {
    console.error(`\x1b[31m[ERROR] Diff analyzer script not found at ${scriptToRun}\x1b[0m`);
    process.exit(1);
  }

  const result = spawnSync("python3", [scriptToRun, ...args], { stdio: "inherit" });
  process.exit(result.status ?? 0);
}

function runCheck() {
  const checkScript = join(ROOT_DIR, "skills", "expected-2-unexpected", "scripts", "self_check.py");
  const fallbackScript = join(ROOT_DIR, "scripts", "self_check.py");
  const scriptToRun = existsSync(checkScript) ? checkScript : fallbackScript;

  if (!existsSync(scriptToRun)) {
    console.error(`\x1b[31m[ERROR] Self-check script not found at ${scriptToRun}\x1b[0m`);
    process.exit(1);
  }

  const result = spawnSync("python3", [scriptToRun], { stdio: "inherit" });
  process.exit(result.status ?? 0);
}

function runInstall() {
  const installScript = join(ROOT_DIR, "install.sh");
  if (!existsSync(installScript)) {
    console.error(`\x1b[31m[ERROR] Installer not found at ${installScript}\x1b[0m`);
    process.exit(1);
  }

  const result = spawnSync("bash", [installScript], { stdio: "inherit" });
  process.exit(result.status ?? 0);
}

function printGuidelines() {
  console.log(BANNER);
  console.log(`\x1b[1mThe Four Non-Negotiable Pillars:\x1b[0m

1. \x1b[32mThink Before Coding\x1b[0m
   - Surface assumptions explicitly. Ask when uncertain.
   - Present multiple interpretations. Do not pick silently.
   - Push back when a simpler path exists.

2. \x1b[32mSimplicity First\x1b[0m
   - Minimum code that solves the problem. Nothing speculative.
   - No single-use abstractions or premature interfaces.
   - Apply the Ponytail Simplicity Ladder: Stop at the first rung that holds.

3. \x1b[32mSurgical Changes\x1b[0m
   - Touch only what you must. Zero adjacent formatting churn.
   - Clean up newly orphaned imports and variables.
   - Every changed line must trace directly to the prompt.

4. \x1b[32mGoal-Driven Execution\x1b[0m
   - Define concrete, verifiable success criteria.
   - 3-step verification plan: [Reproduction] -> [Surgical Edit] -> [Check].
   - Red-green falsification before declaring done.
`);
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0] || "help";

  switch (command) {
    case "audit":
    case "diff-check":
      runAudit(args.slice(1));
      break;
    case "check":
    case "test":
      runCheck();
      break;
    case "install":
      runInstall();
      break;
    case "guidelines":
    case "pillars":
      printGuidelines();
      break;
    case "-v":
    case "--version":
    case "version":
      console.log("expected-2-unexpected v1.0.0");
      break;
    case "-h":
    case "--help":
    case "help":
    default:
      printHelp();
      break;
  }
}

main();
