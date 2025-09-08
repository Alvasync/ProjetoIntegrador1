/**
 * Componente 3D de Casa Interativa
 * Desenvolvido para o TCC - Análise e Desenvolvimento de Sistemas
 * 
 * Este arquivo implementa uma mini casa em 3D que reage à rolagem da página
 * usando a biblioteca Three.js
 */

class ThreeDHouse {
    constructor(containerId = 'threejs-container') {
        this.containerId = containerId;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.house = null;
        this.animationId = null;
        this.scrollY = 0;
        this.targetRotation = { x: 0, y: 0, z: 0 };
        this.currentRotation = { x: 0, y: 0, z: 0 };
        
        this.init();
    }
    
    init() {
        this.createContainer();
        this.setupScene();
        this.createHouse();
        this.setupLights();
        this.setupEventListeners();
        this.animate();
    }
    
    createContainer() {
        // Criar container se não existir
        let container = document.getElementById(this.containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = this.containerId;
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                width: 200px;
                height: 200px;
                z-index: 1000;
                border-radius: 15px;
                overflow: hidden;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                pointer-events: none;
                transition: opacity 0.3s ease;
            `;
            document.body.appendChild(container);
        }
        this.container = container;
    }
    
    setupScene() {
        // Criar cena
        this.scene = new THREE.Scene();
        this.scene.background = null; // Fundo transparente
        
        // Criar câmera
        this.camera = new THREE.PerspectiveCamera(
            75, 
            this.container.clientWidth / this.container.clientHeight, 
            0.1, 
            1000
        );
        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);
        
        // Criar renderizador
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true, 
            alpha: true 
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setClearColor(0x000000, 0); // Fundo transparente
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        this.container.appendChild(this.renderer.domElement);
    }
    
    createHouse() {
        this.house = new THREE.Group();
        
        // Cores modernas
        const colors = {
            wall: 0xf5f5f5,      // Branco suave
            roof: 0x8b4513,      // Marrom
            door: 0x654321,      // Marrom escuro
            window: 0x87ceeb,    // Azul claro
            foundation: 0x708090  // Cinza
        };
        
        // Base/Fundação
        const foundationGeometry = new THREE.BoxGeometry(3.2, 0.2, 2.2);
        const foundationMaterial = new THREE.MeshLambertMaterial({ color: colors.foundation });
        const foundation = new THREE.Mesh(foundationGeometry, foundationMaterial);
        foundation.position.y = -0.6;
        foundation.castShadow = true;
        foundation.receiveShadow = true;
        this.house.add(foundation);
        
        // Paredes principais
        const wallGeometry = new THREE.BoxGeometry(3, 2, 2);
        const wallMaterial = new THREE.MeshLambertMaterial({ color: colors.wall });
        const walls = new THREE.Mesh(wallGeometry, wallMaterial);
        walls.position.y = 0.5;
        walls.castShadow = true;
        walls.receiveShadow = true;
        this.house.add(walls);
        
        // Telhado
        const roofGeometry = new THREE.ConeGeometry(2.2, 1.5, 4);
        const roofMaterial = new THREE.MeshLambertMaterial({ color: colors.roof });
        const roof = new THREE.Mesh(roofGeometry, roofMaterial);
        roof.position.y = 2.25;
        roof.rotation.y = Math.PI / 4;
        roof.castShadow = true;
        this.house.add(roof);
        
        // Porta
        const doorGeometry = new THREE.BoxGeometry(0.6, 1.2, 0.05);
        const doorMaterial = new THREE.MeshLambertMaterial({ color: colors.door });
        const door = new THREE.Mesh(doorGeometry, doorMaterial);
        door.position.set(0, -0.1, 1.025);
        this.house.add(door);
        
        // Janelas
        const windowGeometry = new THREE.BoxGeometry(0.8, 0.6, 0.05);
        const windowMaterial = new THREE.MeshLambertMaterial({ color: colors.window });
        
        // Janela esquerda
        const windowLeft = new THREE.Mesh(windowGeometry, windowMaterial);
        windowLeft.position.set(-0.8, 0.5, 1.025);
        this.house.add(windowLeft);
        
        // Janela direita
        const windowRight = new THREE.Mesh(windowGeometry, windowMaterial);
        windowRight.position.set(0.8, 0.5, 1.025);
        this.house.add(windowRight);
        
        // Janela lateral
        const windowSide = new THREE.Mesh(windowGeometry, windowMaterial);
        windowSide.position.set(1.525, 0.5, 0);
        windowSide.rotation.y = -Math.PI / 2;
        this.house.add(windowSide);
        
        // Chaminé
        const chimneyGeometry = new THREE.BoxGeometry(0.3, 1, 0.3);
        const chimneyMaterial = new THREE.MeshLambertMaterial({ color: 0x8b0000 });
        const chimney = new THREE.Mesh(chimneyGeometry, chimneyMaterial);
        chimney.position.set(0.8, 2.5, -0.5);
        chimney.castShadow = true;
        this.house.add(chimney);
        
        // Adicionar detalhes decorativos
        this.addDecorations();
        
        this.scene.add(this.house);
    }
    
    addDecorations() {
        // Pequeno jardim na frente
        const grassGeometry = new THREE.CylinderGeometry(1.8, 1.8, 0.1, 8);
        const grassMaterial = new THREE.MeshLambertMaterial({ color: 0x90ee90 });
        const grass = new THREE.Mesh(grassGeometry, grassMaterial);
        grass.position.set(0, -0.55, 1.5);
        grass.receiveShadow = true;
        this.house.add(grass);
        
        // Árvore pequena
        const trunkGeometry = new THREE.CylinderGeometry(0.05, 0.08, 0.6);
        const trunkMaterial = new THREE.MeshLambertMaterial({ color: 0x8b4513 });
        const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
        trunk.position.set(-2, -0.2, 1.5);
        trunk.castShadow = true;
        this.house.add(trunk);
        
        const leavesGeometry = new THREE.SphereGeometry(0.4);
        const leavesMaterial = new THREE.MeshLambertMaterial({ color: 0x228b22 });
        const leaves = new THREE.Mesh(leavesGeometry, leavesMaterial);
        leaves.position.set(-2, 0.3, 1.5);
        leaves.castShadow = true;
        this.house.add(leaves);
    }
    
    setupLights() {
        // Luz ambiente
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Luz direcional (sol)
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        
        // Configurar sombras
        directionalLight.shadow.mapSize.width = 1024;
        directionalLight.shadow.mapSize.height = 1024;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 50;
        directionalLight.shadow.camera.left = -10;
        directionalLight.shadow.camera.right = 10;
        directionalLight.shadow.camera.top = 10;
        directionalLight.shadow.camera.bottom = -10;
        
        this.scene.add(directionalLight);
        
        // Luz pontual colorida para efeito
        const pointLight = new THREE.PointLight(0x4a90e2, 0.3, 20);
        pointLight.position.set(-5, 5, 5);
        this.scene.add(pointLight);
    }
    
    setupEventListeners() {
        // Listener para scroll
        window.addEventListener('scroll', (e) => {
            this.scrollY = window.pageYOffset;
            this.updateRotationFromScroll();
        });
        
        // Listener para resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Hover effects (opcional)
        this.container.addEventListener('mouseenter', () => {
            this.container.style.transform = 'scale(1.05)';
        });
        
        this.container.addEventListener('mouseleave', () => {
            this.container.style.transform = 'scale(1)';
        });
        
        // Responsividade - ocultar em telas pequenas
        this.checkScreenSize();
        window.addEventListener('resize', () => {
            this.checkScreenSize();
        });
    }
    
    updateRotationFromScroll() {
        // Calcular rotação baseada no scroll
        const scrollProgress = this.scrollY * 0.01;
        
        this.targetRotation.x = Math.sin(scrollProgress * 0.5) * 0.2;
        this.targetRotation.y = scrollProgress * 0.3;
        this.targetRotation.z = Math.cos(scrollProgress * 0.3) * 0.1;
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        if (!this.house) return;
        
        // Interpolação suave da rotação
        const ease = 0.05;
        this.currentRotation.x += (this.targetRotation.x - this.currentRotation.x) * ease;
        this.currentRotation.y += (this.targetRotation.y - this.currentRotation.y) * ease;
        this.currentRotation.z += (this.targetRotation.z - this.currentRotation.z) * ease;
        
        // Aplicar rotação
        this.house.rotation.x = this.currentRotation.x;
        this.house.rotation.y = this.currentRotation.y;
        this.house.rotation.z = this.currentRotation.z;
        
        // Pequena animação de flutuação
        const time = Date.now() * 0.001;
        this.house.position.y = Math.sin(time * 0.5) * 0.1;
        
        // Renderizar
        this.renderer.render(this.scene, this.camera);
    }
    
    handleResize() {
        if (!this.camera || !this.renderer) return;
        
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    checkScreenSize() {
        // Ocultar em telas pequenas para não atrapalhar a usabilidade
        if (window.innerWidth < 768) {
            this.container.style.display = 'none';
        } else {
            this.container.style.display = 'block';
        }
    }
    
    destroy() {
        // Cleanup
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        if (this.renderer) {
            this.renderer.dispose();
        }
        
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
        
        // Remover event listeners
        window.removeEventListener('scroll', this.updateRotationFromScroll);
        window.removeEventListener('resize', this.handleResize);
    }
    
    // Métodos públicos para controle
    show() {
        this.container.style.opacity = '1';
    }
    
    hide() {
        this.container.style.opacity = '0';
    }
    
    setPosition(top, right) {
        this.container.style.top = top + 'px';
        this.container.style.right = right + 'px';
    }
}

// Auto-inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se Three.js está carregado
    if (typeof THREE !== 'undefined') {
        // Inicializar a casa 3D
        window.threeDHouse = new ThreeDHouse();
        console.log('Casa 3D inicializada com sucesso!');
    } else {
        console.warn('Three.js não está carregado. A casa 3D não será exibida.');
    }
});

// Exportar para uso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThreeDHouse;
}

if (typeof window !== 'undefined') {
    window.ThreeDHouse = ThreeDHouse;
}
