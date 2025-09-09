/**
 * Sistema 3D Interativo Inspirado no Pioneer
 * Efeitos: Partículas, Rotação, Hover, Click Interactions
 * Modelo: Casa para Precificação Imobiliária
 */

class Interactive3DHouse {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.house = null;
        this.particles = null;
        this.particleSystem = null;
        this.mouse = new THREE.Vector2();
        this.raycaster = new THREE.Raycaster();
        this.isHovering = false;
        this.autoRotate = true;
        this.animationId = null;
        
        // Configurações
        this.config = {
            particleCount: 150,
            connectionDistance: 80,
            mouseInfluence: 100,
            rotationSpeed: 0.002,
            hoverScale: 1.1,
            clickExplosion: 2.0
        };
        
        // Não inicializar automaticamente - será chamado pelo HTML
    }
    
    init() {
        console.log('🎯 Iniciando Interactive3DHouse.init()');
        try {
            console.log('📦 Criando container...');
            this.createContainer();
            
            console.log('🎬 Configurando cena...');
            this.setupScene();
            
            console.log('📷 Configurando câmera...');
            this.setupCamera();
            
            console.log('🖥️ Configurando renderer...');
            this.setupRenderer();
            
            console.log('💡 Configurando luzes...');
            this.setupLights();
            
            console.log('✨ Criando sistema de partículas...');
            this.createParticleSystem();
            
            console.log('🏠 Carregando modelo da casa...');
            this.loadHouseModel();
            
            console.log('🎮 Configurando event listeners...');
            this.setupEventListeners();
            
            console.log('🎥 Iniciando animação...');
            this.animate();
            
            console.log('✅ Interactive3DHouse inicializado com sucesso!');
        } catch (error) {
            console.error('❌ Erro durante inicialização:', error);
        }
    }
    
    createContainer() {
        // Container para o modelo 3D como fundo da página inteira
        const container = document.createElement('div');
        container.id = 'house-3d-container';
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            pointer-events: none;
            background: transparent;
        `;
        
        // Inserir como primeiro elemento do body
        document.body.insertBefore(container, document.body.firstChild);
        
        return container;
    }
    
    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = null; // Transparente para ser fundo
        
        // Fog para profundidade cinematográfica
        this.scene.fog = new THREE.Fog(0x000011, 100, 800);
    }
    
    setupCamera() {
        // Câmera para fullscreen
        const aspect = window.innerWidth / window.innerHeight;
        
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 2000);
        this.camera.position.set(30, 20, 30);
        this.camera.lookAt(0, 0, 0);
    }
    
    setupRenderer() {
        const container = document.getElementById('house-3d-container');
        
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true, 
            alpha: true,
            powerPreference: "high-performance"
        });
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 0.8;
        this.renderer.setClearColor(0x000000, 0);
        
        container.appendChild(this.renderer.domElement);
    }
    
    setupLights() {
        // Luz ambiente um pouco mais forte para ver a cidade
        const ambientLight = new THREE.AmbientLight(0x1a1a2e, 0.4);
        this.scene.add(ambientLight);
        
        // Luz direcional principal (lua)
        const moonLight = new THREE.DirectionalLight(0x9cc5ff, 0.4);
        moonLight.position.set(50, 100, 30);
        moonLight.castShadow = true;
        moonLight.shadow.mapSize.width = 4096;
        moonLight.shadow.mapSize.height = 4096;
        moonLight.shadow.camera.near = 1;
        moonLight.shadow.camera.far = 200;
        moonLight.shadow.camera.left = -100;
        moonLight.shadow.camera.right = 100;
        moonLight.shadow.camera.top = 100;
        moonLight.shadow.camera.bottom = -100;
        this.scene.add(moonLight);
        
        // Luzes de cidade - múltiplas luzes coloridas
        const cityLights = [
            { color: 0x00ffff, pos: [-30, 15, -20], intensity: 0.6 },
            { color: 0xff0080, pos: [25, 10, 30], intensity: 0.5 },
            { color: 0x0080ff, pos: [-15, 20, 40], intensity: 0.4 },
            { color: 0x80ff00, pos: [40, 8, -10], intensity: 0.3 },
            { color: 0xffffff, pos: [0, 30, 0], intensity: 0.8 }
        ];
        
        cityLights.forEach(light => {
            const pointLight = new THREE.PointLight(light.color, light.intensity, 60);
            pointLight.position.set(...light.pos);
            this.scene.add(pointLight);
        });
    }
    
    createParticleSystem() {
        const particleGeometry = new THREE.BufferGeometry();
        const particleCount = 50; // Poucas partículas discretas como no Pioneer
        
        const positions = new Float32Array(particleCount * 3);
        const velocities = new Float32Array(particleCount * 3);
        
        // Distribuir partículas de forma mais espaçada e sutil
        for (let i = 0; i < particleCount * 3; i += 3) {
            // Área controlada ao redor da cidade
            positions[i] = (Math.random() - 0.5) * 120;     // X: -60 a 60
            positions[i + 1] = Math.random() * 40 + 10;     // Y: 10 a 50
            positions[i + 2] = (Math.random() - 0.5) * 120; // Z: -60 a 60
            
            // Velocidades extremamente lentas
            velocities[i] = (Math.random() - 0.5) * 0.002;
            velocities[i + 1] = (Math.random() - 0.5) * 0.001;
            velocities[i + 2] = (Math.random() - 0.5) * 0.002;
        }
        
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
        particleGeometry.setAttribute('originalPosition', new THREE.BufferAttribute(originalPositions, 3));
        
        // Material das partículas com visual suave como no Pioneer
        const particleMaterial = new THREE.PointsMaterial({
            color: 0x4A90E2,
            size: 1.5,
            transparent: true,
            opacity: 0.5,
            vertexColors: false,
            blending: THREE.AdditiveBlending,
            sizeAttenuation: true,
            fog: false
        });
        
        this.particles = new THREE.Points(particleGeometry, particleMaterial);
        this.scene.add(this.particles);
        
        // Sistema simples sem conexões
    }
    
    // Removido sistema de conexões para visual mais limpo
    
    loadHouseModel() {
        // Verificar se GLTFLoader está disponível
        if (!THREE.GLTFLoader) {
            console.error('GLTFLoader não está carregado. Verifique o script.');
            return;
        }
        
        const loader = new THREE.GLTFLoader();
        
        loader.load(
            '/static/models/house.glb',
            (gltf) => {
                this.house = gltf.scene;
                
                // Configurar o modelo como cidade principal
                this.house.scale.set(8, 8, 8);
                this.house.position.set(0, -10, 0);
                
                // Configurar sombras e opacidade visível
                this.house.traverse((child) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                        
                        // Opacidade mais visível mas não totalmente opaca
                        if (child.material) {
                            child.material.transparent = true;
                            child.material.opacity = 0.8;
                            child.material.envMapIntensity = 0.5;
                        }
                    }
                });
                
                this.scene.add(this.house);
                console.log('🏠 Casa 3D carregada com sucesso!');
            },
            (progress) => {
                console.log('Carregando casa 3D:', (progress.loaded / progress.total * 100) + '%');
            },
            (error) => {
                console.error('Erro ao carregar casa 3D:', error);
            }
        );
    }
    
    setupEventListeners() {
        // Mouse events na janela inteira
        window.addEventListener('mousemove', (event) => this.onMouseMove(event), false);
        window.addEventListener('mouseenter', () => this.onMouseEnter(), false);
        window.addEventListener('mouseleave', () => this.onMouseLeave(), false);
        window.addEventListener('click', () => this.onClick(), false);
        
        // Resize
        window.addEventListener('resize', () => this.onWindowResize(), false);
        
        // Scroll para pausar/retomar animação
        window.addEventListener('scroll', () => this.onScroll(), false);
    }
    
    onMouseMove(event) {
        // Mouse normalizado para a janela inteira
        this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        
        // Movimento MUITO sutil da câmera como no Pioneer
        if (this.camera) {
            const targetX = this.mouse.x * 2; // Movimento mínimo
            const targetY = this.mouse.y * 1; // Movimento mínimo
            
            this.camera.position.x += (30 + targetX - this.camera.position.x) * 0.01;
            this.camera.position.y += (20 + targetY - this.camera.position.y) * 0.01;
            this.camera.lookAt(0, 0, 0);
        }
    }
    
    // Partículas com movimento sutil e estático como no Pioneer
    updateParticlesMovement() {
        if (!this.particles) return;
        
        const positions = this.particles.geometry.attributes.position.array;
        const velocities = this.particles.geometry.attributes.velocity.array;
        
        // Movimento muito sutil e lento
        for (let i = 0; i < positions.length; i += 3) {
            positions[i] += velocities[i];
            positions[i + 1] += velocities[i + 1];
            positions[i + 2] += velocities[i + 2];
        }
        
        this.particles.geometry.attributes.position.needsUpdate = true;
    }
    
    onMouseEnter() {
        this.isHovering = true;
        const container = document.getElementById('house-3d-container');
        
        // Efeito hover no container
        container.style.transform = 'translateY(-50%) scale(1.05)';
        container.style.boxShadow = '0 20px 60px rgba(74, 144, 226, 0.4)';
        
        // Acelerar rotação
        this.config.rotationSpeed = 0.005;
        
        // Efeito nas partículas
        if (this.particles) {
            this.particles.material.size = 3;
            this.particles.material.opacity = 1.0;
        }
    }
    
    onMouseLeave() {
        this.isHovering = false;
        const container = document.getElementById('house-3d-container');
        
        // Remover efeito hover
        container.style.transform = 'translateY(-50%) scale(1)';
        container.style.boxShadow = '0 10px 40px rgba(74, 144, 226, 0.2)';
        
        // Velocidade normal
        this.config.rotationSpeed = 0.002;
        
        // Partículas normais
        if (this.particles) {
            this.particles.material.size = 2;
            this.particles.material.opacity = 0.8;
        }
    }
    
    onClick() {
        console.log('🎯 Casa 3D clicada!');
        
        // Efeito de explosão nas partículas
        this.createExplosionEffect();
        
        // Pulso na casa
        if (this.house) {
            const originalScale = this.house.scale.clone();
            
            // Animação de pulso
            const pulseScale = originalScale.clone().multiplyScalar(1.2);
            
            // Usar GSAP se disponível, senão animação manual
            if (window.gsap) {
                gsap.to(this.house.scale, {
                    duration: 0.3,
                    x: pulseScale.x,
                    y: pulseScale.y,
                    z: pulseScale.z,
                    yoyo: true,
                    repeat: 1,
                    ease: "power2.inOut"
                });
            } else {
                // Animação manual
                let progress = 0;
                const animate = () => {
                    progress += 0.1;
                    if (progress <= 1) {
                        const scale = progress < 0.5 ? 
                            originalScale.clone().lerp(pulseScale, progress * 2) :
                            pulseScale.clone().lerp(originalScale, (progress - 0.5) * 2);
                        
                        this.house.scale.copy(scale);
                        requestAnimationFrame(animate);
                    }
                };
                animate();
            }
        }
        
        // Vibração no container
        const container = document.getElementById('house-3d-container');
        container.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            container.style.animation = '';
        }, 500);
    }
    
    createExplosionEffect() {
        if (!this.particles) return;
        
        const positions = this.particles.geometry.attributes.position.array;
        const velocities = this.particles.geometry.attributes.velocity.array;
        
        // Aplicar força explosiva
        for (let i = 0; i < positions.length; i += 3) {
            const x = positions[i];
            const y = positions[i + 1];
            const z = positions[i + 2];
            
            const distance = Math.sqrt(x * x + y * y + z * z);
            const force = this.config.clickExplosion / (distance + 1);
            
            velocities[i] += (x / distance) * force;
            velocities[i + 1] += (y / distance) * force;
            velocities[i + 2] += (z / distance) * force;
        }
        
        // Reset gradual das velocidades
        setTimeout(() => {
            for (let i = 0; i < velocities.length; i++) {
                velocities[i] *= 0.95;
            }
        }, 100);
    }
    
    onWindowResize() {
        if (this.camera && this.renderer) {
            const aspect = window.innerWidth / window.innerHeight;
            this.camera.aspect = aspect;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        }
    }
    
    onScroll() {
        const precificadorSection = document.getElementById('precificador');
        if (!precificadorSection) return;
        
        const rect = precificadorSection.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (!isVisible && this.animationId) {
            // Pausar animação quando não visível
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        } else if (isVisible && !this.animationId) {
            // Retomar animação quando visível
            this.animate();
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Rotação muito lenta da cidade
        if (this.house) {
            this.house.rotation.y += 0.0005; // Rotação muito lenta
        }
        
        // Movimento sutil das partículas
        this.updateParticlesMovement();
        
        // Render
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        const container = document.getElementById('house-3d-container');
        if (container) {
            container.remove();
        }
        
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// CSS para animação de shake
const shakeCSS = `
    @keyframes shake {
        0%, 100% { transform: translateY(-50%) translateX(0); }
        10% { transform: translateY(-50%) translateX(-5px); }
        20% { transform: translateY(-50%) translateX(5px); }
        30% { transform: translateY(-50%) translateX(-5px); }
        40% { transform: translateY(-50%) translateX(5px); }
        50% { transform: translateY(-50%) translateX(-3px); }
        60% { transform: translateY(-50%) translateX(3px); }
        70% { transform: translateY(-50%) translateX(-2px); }
        80% { transform: translateY(-50%) translateX(2px); }
        90% { transform: translateY(-50%) translateX(-1px); }
    }
`;

// Adicionar CSS
const style = document.createElement('style');
style.textContent = shakeCSS;
document.head.appendChild(style);

// Exportar para uso global
window.Interactive3DHouse = Interactive3DHouse;
