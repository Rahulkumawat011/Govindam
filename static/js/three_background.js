/**
 * Govindam Enterprises - 3D Background Animation System
 * Built with Three.js for high-performance 3D ambient particle grids & floating structural shapes
 */

(function () {
    'use strict';

    function init3DBackground() {
        const container = document.getElementById('three-hero-container');
        if (!container) return;

        // Check if Three.js is loaded
        if (typeof THREE === 'undefined') {
            console.warn('Three.js is not loaded. 3D background animation skipped.');
            return;
        }

        // Scene setup
        const scene = new THREE.Scene();
        
        // Camera setup
        const camera = new THREE.PerspectiveCamera(
            60,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
        );
        camera.position.z = 30;

        // Renderer setup
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const pointLight1 = new THREE.PointLight(0x0284c7, 2, 100);
        pointLight1.position.set(20, 20, 20);
        scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0xc5a059, 2.5, 100);
        pointLight2.position.set(-20, -20, 20);
        scene.add(pointLight2);

        // Group for all 3D floating items
        const group3D = new THREE.Group();
        scene.add(group3D);

        // 1. Create Floating 3D Geometries (Wireframe Structural Shapes & Transmission Hardware Nodes)
        const geometries = [
            new THREE.BoxGeometry(2.5, 2.5, 2.5),
            new THREE.OctahedronGeometry(2, 0),
            new THREE.IcosahedronGeometry(1.8, 0),
            new THREE.CylinderGeometry(0.5, 0.5, 4, 8), // Beam shape
            new THREE.TorusGeometry(1.5, 0.4, 8, 24)
        ];

        const materials = [
            new THREE.MeshStandardMaterial({
                color: 0x38bdf8,
                wireframe: true,
                transparent: true,
                opacity: 0.45
            }),
            new THREE.MeshStandardMaterial({
                color: 0xc5a059,
                wireframe: true,
                transparent: true,
                opacity: 0.5
            }),
            new THREE.MeshStandardMaterial({
                color: 0x0284c7,
                roughness: 0.3,
                metalness: 0.8,
                transparent: true,
                opacity: 0.4
            })
        ];

        const meshes = [];
        const numObjects = 18;

        for (let i = 0; i < numObjects; i++) {
            const geom = geometries[Math.floor(Math.random() * geometries.length)];
            const mat = materials[Math.floor(Math.random() * materials.length)];
            const mesh = new THREE.Mesh(geom, mat);

            // Random positions in 3D space
            mesh.position.x = (Math.random() - 0.5) * 50;
            mesh.position.y = (Math.random() - 0.5) * 35;
            mesh.position.z = (Math.random() - 0.5) * 30;

            // Random rotation speeds
            mesh.userData = {
                rotSpeedX: (Math.random() - 0.5) * 0.015,
                rotSpeedY: (Math.random() - 0.5) * 0.015,
                rotSpeedZ: (Math.random() - 0.5) * 0.015,
                floatSpeed: 0.005 + Math.random() * 0.01,
                floatOffset: Math.random() * Math.PI * 2,
                initialY: mesh.position.y
            };

            group3D.add(mesh);
            meshes.push(mesh);
        }

        // 2. Create Glowing 3D Particle Constellation (Electrical Grid Nodes)
        const particleCount = 160;
        const particleGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);

        const colorGold = new THREE.Color(0xc5a059);
        const colorCyan = new THREE.Color(0x38bdf8);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 70;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 45;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 40;

            const mixedColor = Math.random() > 0.5 ? colorGold : colorCyan;
            colors[i * 3] = mixedColor.r;
            colors[i * 3 + 1] = mixedColor.g;
            colors[i * 3 + 2] = mixedColor.b;
        }

        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const particleMaterial = new THREE.PointsMaterial({
            size: 0.8,
            vertexColors: true,
            transparent: true,
            opacity: 0.75
        });

        const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
        group3D.add(particleSystem);

        // 3. Mouse Interaction & Camera Parallax
        let mouseX = 0;
        let mouseY = 0;
        let targetMouseX = 0;
        let targetMouseY = 0;

        const windowHalfX = window.innerWidth / 2;
        const windowHalfY = window.innerHeight / 2;

        function onMouseMove(event) {
            targetMouseX = (event.clientX - windowHalfX) * 0.0015;
            targetMouseY = (event.clientY - windowHalfY) * 0.0015;
        }

        window.addEventListener('mousemove', onMouseMove, { passive: true });

        // 4. Animation Loop
        let clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);

            const elapsedTime = clock.getElapsedTime();

            // Smooth mouse interpolation
            mouseX += (targetMouseX - mouseX) * 0.05;
            mouseY += (targetMouseY - mouseY) * 0.05;

            // Rotate main 3D group based on mouse position
            group3D.rotation.y = elapsedTime * 0.04 + mouseX;
            group3D.rotation.x = mouseY * 0.5;

            // Animate individual meshes (floating + rotating)
            meshes.forEach(mesh => {
                mesh.rotation.x += mesh.userData.rotSpeedX;
                mesh.rotation.y += mesh.userData.rotSpeedY;
                mesh.rotation.z += mesh.userData.rotSpeedZ;

                // Floating up & down sin wave
                mesh.position.y = mesh.userData.initialY + Math.sin(elapsedTime * 1.5 + mesh.userData.floatOffset) * 1.2;
            });

            // Animate particle wave motion
            const particlePositions = particleGeometry.attributes.position.array;
            for (let i = 0; i < particleCount; i++) {
                const i3 = i * 3;
                particlePositions[i3 + 1] += Math.sin(elapsedTime * 2 + particlePositions[i3]) * 0.008;
            }
            particleGeometry.attributes.position.needsUpdate = true;

            // Render 3D Scene
            renderer.render(scene, camera);
        }

        animate();

        // 5. Handle Window Resize
        function onWindowResize() {
            if (!container) return;
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }

        window.addEventListener('resize', onWindowResize, false);
    }

    // Initialize when DOM content is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init3DBackground);
    } else {
        init3DBackground();
    }
})();
