const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '..', 'frontend');
const distDir = path.join(__dirname, '..', 'dist');

console.log('Building Project ORCA Marine Platform static assets...');

// Clean or create dist directory
if (fs.existsSync(distDir)) {
  fs.rmSync(distDir, { recursive: true, force: true });
}
fs.mkdirSync(distDir, { recursive: true });

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
    const entries = fs.readdirSync(src);
    for (const entry of entries) {
      if (['node_modules', '.git', 'package.json', 'package-lock.json'].includes(entry)) continue;
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.copyFileSync(src, dest);
  }
}

copyRecursive(srcDir, distDir);
console.log('✓ Build successful! Production assets compiled to /dist');
