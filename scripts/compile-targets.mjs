// Compile card front images into targets.mind via mind-ar's OfflineCompiler.
// Run: node scripts/compile-targets.mjs <img1> [img2] ...
import { loadImage } from 'canvas';
import { writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { OfflineCompiler } from 'mind-ar/src/image-target/offline-compiler.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const OUT = resolve(ROOT, 'targets', 'targets.mind');

const argv = process.argv.slice(2);
if (argv.length === 0) {
  console.error('Usage: node scripts/compile-targets.mjs <image>...');
  process.exit(1);
}

const images = [];
for (const p of argv) {
  const img = await loadImage(resolve(p));
  console.log(`  loaded ${p} (${img.width}x${img.height})`);
  images.push(img);
}

const compiler = new OfflineCompiler();
console.log('Compiling targets...');
let lastPct = -1;
await compiler.compileImageTargets(images, (pct) => {
  const rounded = Math.floor(pct);
  if (rounded > lastPct) {
    process.stdout.write(`\r  ${rounded}%`);
    lastPct = rounded;
  }
});
process.stdout.write('\n');

const buffer = compiler.exportData();
writeFileSync(OUT, Buffer.from(buffer));
const sizeKb = (buffer.length / 1024).toFixed(1);
console.log(`  wrote ${OUT} (${sizeKb} KB)`);
