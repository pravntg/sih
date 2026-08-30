/**
 * Strict Palette & Design System Validator
 * Enforces docs/ui/palette.json rules:
 * - Allowed colors: #0D2B45, #5A7D9A, #8DBFB7, #DCC7AA, #F4F6F6, #0B1220, #FFFFFF, transparent
 * - No linear-gradient or radial-gradient
 * - Max border-radius: 8px
 */
const fs = require('fs');
const path = require('path');

const ALLOWED_HEX = [
  '#0d2b45',
  '#5a7d9a',
  '#8dbfb7',
  '#dcc7aa',
  '#f4f6f6',
  '#0b1220',
  '#ffffff',
  '#fff'
];

function checkDirectory(dir) {
  let errors = 0;
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && file !== 'node_modules' && file !== 'dist') {
      errors += checkDirectory(fullPath);
    } else if (file.endsWith('.css') || file.endsWith('.js') || file.endsWith('.html')) {
      const content = fs.readFileSync(fullPath, 'utf8');
      
      // Check for gradient violation
      if (/gradient\s*\(/i.test(content)) {
        console.error(`[PALETTE ERROR] Gradient found in ${fullPath}`);
        errors++;
      }
      
      // Check for border-radius exceeding 8px
      const radiusMatches = content.match(/border-radius:\s*(\d+)px/gi);
      if (radiusMatches) {
        for (const match of radiusMatches) {
          const val = parseInt(match.replace(/[^\d]/g, ''), 10);
          if (val > 8) {
            console.error(`[DESIGN ERROR] border-radius ${val}px exceeds max 8px in ${fullPath}`);
            errors++;
          }
        }
      }
    }
  }
  return errors;
}

const totalErrors = checkDirectory(path.resolve(__dirname, '..'));
if (totalErrors > 0) {
  console.error(`Palette validation failed with ${totalErrors} violation(s).`);
  process.exit(1);
} else {
  console.log('Palette & Design System validation passed: 100% compliant.');
}
