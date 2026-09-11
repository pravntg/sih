/**
 * Project ORCA — Thermal Wind & Oceanic Current Streamline Particle Engine
 * High-performance 60 FPS Canvas overlay for Leaflet maps.
 * Universal Scientific Researcher Color Scale (NOAA / ECMWF / Earth Nullschool standard).
 */

// Universal Scientific Colormap for Oceanic & Atmospheric Velocity Fields
const SCIENTIFIC_COLOR_SCALE = [
  { maxSpeed: 10, color: '#2B83BA', label: '< 10 km/h (Calm)' },        // Deep Marine Blue
  { maxSpeed: 25, color: '#66C2A5', label: '10–25 km/h (Light)' },      // Aquamarine
  { maxSpeed: 40, color: '#FEE08B', label: '25–40 km/h (Fresh)' },      // Solar Amber/Gold
  { maxSpeed: 60, color: '#FDAE61', label: '40–60 km/h (Near Gale)' },  // Thermal Orange
  { maxSpeed: 999, color: '#D53E4F', label: '> 60 km/h (Storm)' }       // Crimson Red
];

function getScientificWindColor(speedKmh) {
  for (const step of SCIENTIFIC_COLOR_SCALE) {
    if (speedKmh <= step.maxSpeed) {
      return step.color;
    }
  }
  return '#D53E4F';
}

export class ThermalWindParticleCanvas {
  constructor(map, options = {}) {
    this.map = map;
    this.particleCount = options.particleCount || 2200;
    this.fadeAlpha = options.fadeAlpha || 0.94; // Trail persistence
    this.speedFactor = options.speedFactor || 0.65;
    this.lineWidth = options.lineWidth || 1.8;
    this.enabled = true;

    this.canvas = null;
    this.ctx = null;
    this.animationFrameId = null;
    this.particles = [];
    this.bounds = null;

    this.initCanvas();
    this.bindEvents();
    this.resetParticles();
    this.startAnimation();
  }

  initCanvas() {
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'wind-particle-canvas';
    this.canvas.style.position = 'absolute';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.pointerEvents = 'none';
    this.canvas.style.zIndex = '450'; // Above tile layer, below markers

    const mapPane = this.map.getPanes().overlayPane;
    mapPane.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    this.resizeCanvas();
  }

  bindEvents() {
    this.map.on('move', () => this.onMapMove());
    this.map.on('moveend', () => this.onMapMoveEnd());
    this.map.on('resize', () => this.resizeCanvas());
  }

  resizeCanvas() {
    const size = this.map.getSize();
    this.canvas.width = size.x;
    this.canvas.height = size.y;
    this.updateCanvasPosition();
  }

  updateCanvasPosition() {
    const topLeft = this.map.containerPointToLayerPoint([0, 0]);
    L.DomUtil.setPosition(this.canvas, topLeft);
  }

  onMapMove() {
    this.updateCanvasPosition();
  }

  onMapMoveEnd() {
    this.resizeCanvas();
    this.resetParticles();
  }

  resetParticles() {
    const size = this.map.getSize();
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push(this.createParticle(size.x, size.y));
    }
  }

  createParticle(width, height) {
    const x = Math.random() * width;
    const y = Math.random() * height;
    const maxAge = 30 + Math.floor(Math.random() * 50);
    return {
      x: x,
      y: y,
      oldX: x,
      oldY: y,
      age: Math.floor(Math.random() * maxAge),
      maxAge: maxAge,
      speed: 0
    };
  }

  /**
   * Evaluates global atmospheric vector field (U = East-West, V = North-South)
   * at given Geographic Coordinates (lat, lon) incorporating Trade Winds & Thermal Gradients.
   */
  getVectorAtLatLng(lat, lon) {
    const absLat = Math.abs(lat);
    
    // 1. Zonal Atmospheric Circulation (Hadley / Ferrel / Polar cells)
    let u = 0; // m/s (Eastward positive)
    let v = 0; // m/s (Northward positive)

    if (absLat < 30) {
      // Tropical Trade Winds (Easterlies: blow East to West, u < 0)
      u = -4.5 - Math.cos(lat * Math.PI / 30) * 3.5;
      v = (lat >= 0 ? -1.8 : 1.8) * Math.sin(lat * Math.PI / 30);
    } else if (absLat >= 30 && absLat < 60) {
      // Mid-Latitude Westerlies (blow West to East, u > 0)
      u = 6.0 + Math.sin((absLat - 30) * Math.PI / 30) * 4.5;
      v = (lat >= 0 ? 2.5 : -2.5) * Math.cos((absLat - 30) * Math.PI / 30);
    } else {
      // Polar Easterlies
      u = -3.0 - Math.sin((absLat - 60) * Math.PI / 30) * 2.0;
      v = (lat >= 0 ? -1.5 : 1.5);
    }

    // 2. Local Thermal Wave & Coastal Eddy Perturbation
    const thermalPerturbationX = Math.sin(lat * 0.35 + lon * 0.25) * 2.2;
    const thermalPerturbationY = Math.cos(lon * 0.40 - lat * 0.20) * 2.0;
    u += thermalPerturbationX;
    v += thermalPerturbationY;

    const speedMs = Math.sqrt(u * u + v * v);
    const speedKmh = speedMs * 3.6; // convert m/s to km/h

    return { u, v, speedKmh };
  }

  startAnimation() {
    const render = () => {
      if (this.enabled) {
        this.drawFrame();
      }
      this.animationFrameId = requestAnimationFrame(render);
    };
    render();
  }

  drawFrame() {
    if (!this.ctx || !this.map) return;

    const size = this.map.getSize();
    const width = size.x;
    const height = size.y;

    // Fade existing trails for smooth streaming effect
    this.ctx.globalCompositeOperation = 'destination-in';
    this.ctx.fillStyle = `rgba(0, 0, 0, ${this.fadeAlpha})`;
    this.ctx.fillRect(0, 0, width, height);

    this.ctx.globalCompositeOperation = 'source-over';
    this.ctx.lineWidth = this.lineWidth;

    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      if (p.age >= p.maxAge || p.x < 0 || p.x > width || p.y < 0 || p.y > height) {
        // Recycle particle to a random screen position
        p.x = Math.random() * width;
        p.y = Math.random() * height;
        p.oldX = p.x;
        p.oldY = p.y;
        p.age = 0;
        p.maxAge = 35 + Math.floor(Math.random() * 45);
        continue;
      }

      // Convert Screen Pixel to Lat/Lng
      const containerPoint = L.point(p.x, p.y);
      const latLng = this.map.containerPointToLatLng(containerPoint);

      // Fetch dynamic vector at coordinate
      const { u, v, speedKmh } = this.getVectorAtLatLng(latLng.lat, latLng.lng);
      p.speed = speedKmh;

      // Project physical velocity displacement into screen space
      const nextLatLng = L.latLng(
        latLng.lat + (v * 0.0035 * this.speedFactor),
        latLng.lng + (u * 0.0035 * this.speedFactor)
      );
      const nextPoint = this.map.latLngToContainerPoint(nextLatLng);

      p.oldX = p.x;
      p.oldY = p.y;
      p.x = nextPoint.x;
      p.y = nextPoint.y;
      p.age++;

      // Render line segment with Scientific Color
      this.ctx.beginPath();
      this.ctx.strokeStyle = getScientificWindColor(p.speed);
      this.ctx.moveTo(p.oldX, p.oldY);
      this.ctx.lineTo(p.x, p.y);
      this.ctx.stroke();
    }
  }

  toggle(enable) {
    this.enabled = enable;
    if (!this.enabled && this.ctx) {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
  }

  setSpeedFactor(factor) {
    this.speedFactor = factor;
  }

  setParticleCount(count) {
    this.particleCount = count;
    this.resetParticles();
  }

  destroy() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.canvas && this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas);
    }
  }
}
