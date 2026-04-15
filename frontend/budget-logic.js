const CURRENT_USER_ID = 1; // Placeholder until login logic is added

// Fetch goals from backend and group by category
const fetchBudgetData = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/goals/${CURRENT_USER_ID}`);
        if (!response.ok) throw new Error("Failed to fetch goals");
        
        const goals = await response.json();
        
        // Group goals by category and calculate totals
        const categories = {};
        
        goals.forEach(goal => {
            const parts = goal.goal_name.split(": ");
            const category = parts[0] || "Other";
            
            if (!categories[category]) {
                categories[category] = {
                    category: category,
                    budgeted: 0,
                    spent: 0,
                    goals: []
                };
            }
            
            categories[category].budgeted += goal.target_amount;
            categories[category].spent += goal.current_amount;
            categories[category].goals.push(goal);
        });
        
        return Object.values(categories);
    } catch (error) {
        console.error("Error fetching budget data:", error);
        // Return sample data as fallback
        return [
            { category: "Housing", budgeted: 1500, spent: 1200, goals: [] },
            { category: "Groceries", budgeted: 600, spent: 650, goals: [] },
            { category: "Entertainment", budgeted: 200, spent: 50, goals: [] },
            { category: "Utilities", budgeted: 300, spent: 280, goals: [] },
            { category: "Savings", budgeted: 500, spent: 500, goals: [] }
        ];
    }
};

// Update goal amount in database
const updateGoalAmount = async (goalId, newCurrentAmount) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/goals/${goalId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                current_amount: newCurrentAmount
            })
        });
        
        if (!response.ok) {
            throw new Error("Failed to update goal");
        }
        
        return true;
    } catch (error) {
        console.error("Error updating goal:", error);
        alert("Could not update goal. Make sure the backend is running.");
        return false;
    }
};

// Refresh the budget display
const refreshBudgetDisplay = async () => {
    const budgetData = await fetchBudgetData();
    const container = document.getElementById("budget-list-container");
    container.innerHTML = ""; // Clear existing content
    
    budgetData.forEach(item => {
        const percent = Math.min((item.spent / item.budgeted) * 100, 100);
        const isOver = item.spent > item.budgeted;

        const row = document.createElement("div");
        row.className = "budget-row";

        row.innerHTML = `
            <div class="budget-info">
                <span>${item.category}</span>
                <span>$${item.spent.toFixed(2)} / $${item.budgeted.toFixed(2)}</span>
            </div>
            <div class="progress-bg">
                <div class="progress-fill ${isOver ? 'over-budget' : ''}" 
                     style="width: ${percent}%"></div>
            </div>
            <p style="font-size: 12px; margin-top: 5px; color: ${isOver ? '#ff69b4' : '#666'}">
                ${isOver ? 'Over budget by $' + (item.spent - item.budgeted).toFixed(2) : (100 - percent).toFixed(0) + '% remaining'}
            </p>
            <div class="edit-controls" style="margin-top: 12px; display: flex; gap: 8px; align-items: center;">
                <button class="edit-btn edit-subtract" onclick="handleAmountChange('${item.category}', -10)">- $10</button>
                <button class="edit-btn edit-add" onclick="handleAmountChange('${item.category}', 10)">+ $10</button>
                <input type="number" class="edit-input" id="amount-${item.category}" placeholder="Amount" step="0.01">
                <button class="edit-btn edit-custom" onclick="handleCustomAmount('${item.category}')">Update</button>
            </div>
        `;

        row.id = `row-${item.category}`;
        container.appendChild(row);
    });
};

// Handle predefined amount changes
const handleAmountChange = async (category, amount) => {
    const budgetData = await fetchBudgetData();
    const categoryData = budgetData.find(b => b.category === category);
    
    if (categoryData && categoryData.goals.length > 0) {
        const goal = categoryData.goals[0]; // Update first goal in category
        const newAmount = Math.max(0, goal.current_amount + amount);
        
        // Update database
        const success = await updateGoalAmount(goal.goal_id, newAmount);
        if (success) {
            await refreshBudgetDisplay();
        }
    }
};

// Handle custom amount input
const handleCustomAmount = async (category) => {
    const input = document.getElementById(`amount-${category}`);
    const amount = parseFloat(input.value);
    
    if (isNaN(amount) || amount < 0) {
        alert("Please enter a valid amount");
        return;
    }
    
    const budgetData = await fetchBudgetData();
    const categoryData = budgetData.find(b => b.category === category);
    
    if (categoryData && categoryData.goals.length > 0) {
        const goal = categoryData.goals[0]; // Update first goal in category
        
        // Update database
        const success = await updateGoalAmount(goal.goal_id, amount);
        if (success) {
            input.value = "";
            await refreshBudgetDisplay();
        }
    }
};

document.addEventListener("DOMContentLoaded", refreshBudgetDisplay);