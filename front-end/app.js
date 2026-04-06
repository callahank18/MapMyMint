// MOBILE STATE
let state = {
    currentTab: 'dashboard',
    transactions: [
        { id: 1, desc: "Starbucks", amount: -6.50, category: "Food" },
        { id: 2, desc: "Refund", amount: 20.00, category: "Misc" }
    ]
};

// MOBILE COMPONENTS
const BottomNav = () => `
    <nav class="bottom-nav">
        <button onclick="switchTab('dashboard')">🏠</button>
        <button onclick="switchTab('add')">➕</button>
        <button onclick="switchTab('history')">📜</button>
    </nav>
`;

const Dashboard = () => `
    <div class="card">
        <h2>Remaining Balance</h2>
        <h1>$${calculateTotal()}</h1>
    </div>
`;

// FRAMEWORK ENGINE
window.switchTab = (tab) => {
    state.currentTab = tab;
    render();
};

function calculateTotal() {
    return state.transactions.reduce((acc, t) => acc + t.amount, 0).toFixed(2);
}

export const render = () => {
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="mobile-wrapper">
            ${state.currentTab === 'dashboard' ? Dashboard() : '<h3>Other Page Content</h3>'}
            ${BottomNav()}
        </div>
    `;
};

render();
