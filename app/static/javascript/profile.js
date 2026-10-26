document.querySelectorAll('[data-copy-profile]').forEach((button) => {
    button.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(button.dataset.copyProfile);
            const originalText = button.textContent;
            button.textContent = 'Link kopiert';
            window.setTimeout(() => { button.textContent = originalText; }, 1800);
        } catch {
            window.prompt('Profil-Link kopieren:', button.dataset.copyProfile);
        }
    });
});

const pictureInput = document.querySelector('input[name="profile_pic"]');
const profileAvatar = document.querySelector('.profile-overview .profile-avatar');
if (pictureInput && profileAvatar) {
    pictureInput.addEventListener('change', () => {
        const file = pictureInput.files[0];
        if (file) profileAvatar.src = URL.createObjectURL(file);
    });
}

const deleteForm = document.getElementById('deleteAccountForm');
if (deleteForm) {
    deleteForm.addEventListener('submit', (event) => {
        if (!window.confirm('Konto und zugehörige Daten endgültig löschen? Diese Aktion kann nicht rückgängig gemacht werden.')) {
            event.preventDefault();
        }
    });
}

const svgNamespace = 'http://www.w3.org/2000/svg';
function addSvgElement(parent, tagName, attributes, text) {
    const element = document.createElementNS(svgNamespace, tagName);
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
    if (text) element.textContent = text;
    parent.appendChild(element);
    return element;
}

document.querySelectorAll('.skill-graph[data-graph]').forEach((graphElement) => {
    let graph;
    try {
        graph = JSON.parse(graphElement.dataset.graph);
    } catch {
        return;
    }

    const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
    const edges = Array.isArray(graph.edges) ? graph.edges : [];
    if (!nodes.length) return;

    const width = 960;
    const columns = Math.min(6, nodes.length);
    const rows = Math.ceil(nodes.length / columns);
    const height = Math.max(260, rows * 88 + 32);
    const positions = new Map();
    graphElement.setAttribute('viewBox', `0 0 ${width} ${height}`);
    graphElement.style.height = `${height}px`;

    nodes.forEach((node, index) => {
        const column = index % columns;
        const row = Math.floor(index / columns);
        const x = columns === 1 ? width / 2 : 70 + column * ((width - 140) / (columns - 1));
        const y = 42 + row * 88;
        positions.set(node.skill, { x, y });
    });

    edges.forEach((edge) => {
        const from = positions.get(edge.from_skill);
        const to = positions.get(edge.to_skill);
        if (from && to) addSvgElement(graphElement, 'line', { x1: from.x, y1: from.y, x2: to.x, y2: to.y, class: 'graph-edge' });
    });

    nodes.forEach((node) => {
        const position = positions.get(node.skill);
        const level = Math.max(0, Math.min(100, Number(node.level) || 0));
        const radius = 14 + level * 0.1;
        const group = addSvgElement(graphElement, 'g', { 'aria-label': `${node.skill}, ${level} Skillpunkte` });
        addSvgElement(group, 'circle', { cx: position.x, cy: position.y, r: radius, class: 'graph-node' });
        addSvgElement(group, 'circle', { cx: position.x, cy: position.y, r: Math.max(3, radius * 0.27), class: 'graph-node-core' });
        addSvgElement(group, 'text', { x: position.x, y: position.y + radius + 17, class: 'graph-label' }, node.skill.length > 17 ? `${node.skill.slice(0, 16)}…` : node.skill);
        addSvgElement(group, 'text', { x: position.x, y: position.y + radius + 30, class: 'graph-level' }, `${level} Punkte`);
        addSvgElement(group, 'title', {}, `${node.skill} · ${node.category} · ${level} Punkte`);
    });
});