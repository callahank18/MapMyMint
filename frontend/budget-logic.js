document.addEventListener("DOMContentLoaded", () => {
    const budgetData = [
        { category: "Housing", budgeted: 1500, spent: 1200 },
        { category: "Groceries", budgeted: 600, spent: 650 }, // Over budget example
        { category: "Entertainment", budgeted: 200, spent: 50 },
        { category: "Utilities", budgeted: 300, spent: 280 },
        { category: "Savings", budgeted: 500, spent: 500 }
    ];

    const container = document.getElementById("budget-list-container");

    budgetData.forEach(item => {
        const percent = Math.min((item.spent / item.budgeted) * 100, 100);
        const isOver = item.spent > item.budgeted;

        const row = document.createElement("div");
        row.className = "budget-row";

        row.innerHTML = `
            <div class="budget-info">
                <span>${item.category}</span>
                <span>$${item.spent} / $${item.budgeted}</span>
            </div>
            <div class="progress-bg">
                <div class="progress-fill ${isOver ? 'over-budget' : ''}" 
                     style="width: ${percent}%"></div>
            </div>
            <p style="font-size: 12px; margin-top: 5px; color: ${isOver ? '#ff69b4' : '#666'}">
                ${isOver ? 'Over budget by $' + (item.spent - item.budgeted) : (100 - percent).toFixed(0) + '% remaining'}
            </p>
        `;

        container.appendChild(row);
    });
});