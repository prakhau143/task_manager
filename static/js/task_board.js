window.initTaskBoard = function (containerId, tasks) {
  const container = document.getElementById(containerId);
  if (!container || !window.THREE) return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  container.innerHTML = "";
  container.appendChild(renderer.domElement);

  const ambient = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambient);

  const directional = new THREE.DirectionalLight(0xffffff, 0.6);
  directional.position.set(5, 10, 7);
  scene.add(directional);

  const statusColors = {
    todo: 0x3b82f6, // blue
    in_progress: 0xfacc15, // yellow
    done: 0x22c55e, // green
    blocked: 0xef4444, // red
  };

  const cubes = [];
  const perRow = 5;

  tasks.slice(0, 10).forEach((task, index) => {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const color =
      statusColors[task.status] !== undefined
        ? statusColors[task.status]
        : 0x94a3b8;
    const material = new THREE.MeshStandardMaterial({
      color,
      metalness: 0.4,
      roughness: 0.3,
    });
    const cube = new THREE.Mesh(geometry, material);

    const row = Math.floor(index / perRow);
    const col = index % perRow;
    // Fixed 2x5 grid (10 cubes max):
    // Row 1 z=0, Row 2 z=-3
    // x = (col - 2) * 3  => -6,-3,0,3,6
    // z = -row * 3       => 0,-3
    cube.position.set((col - 2) * 3, 0, -row * 3);

    cube.userData = task;
    scene.add(cube);
    cubes.push(cube);
  });

  camera.position.set(0, 6, 12);
  camera.lookAt(0, 0, -1.5);

  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  let hovered = null;

  function onMouseMove(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  }

  renderer.domElement.addEventListener("mousemove", onMouseMove);

  renderer.domElement.addEventListener("click", () => {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(cubes);
    if (intersects.length) {
      const task = intersects[0].object.userData;
      if (task && task.id) {
        window.location.href = `/tasks/${task.id}/`;
      }
    }
  });

  window.addEventListener("resize", () => {
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
  });

  function animate() {
    requestAnimationFrame(animate);

    cubes.forEach((cube) => {
      // Smooth, slow rotation only (no floating movement).
      cube.rotation.y += 0.006;
      cube.rotation.x += 0.0025;
    });

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(cubes);

    if (hovered && (!intersects.length || intersects[0].object !== hovered)) {
      hovered.scale.set(1, 1, 1);
      hovered = null;
    }

    if (intersects.length) {
      const obj = intersects[0].object;
      if (hovered !== obj) {
        if (hovered) hovered.scale.set(1, 1, 1);
        hovered = obj;
        hovered.scale.set(1.25, 1.25, 1.25);
      }
    }

    renderer.render(scene, camera);
  }

  animate();
};

