/**
 * MapMyMint - D3 Sunburst Logic
 * Responsive, Hierarchical Budget Visualization
 */

const CURRENT_USER_ID = 1; // Placeholder until login logic is added

// Fetch goals from the backend and transform into hierarchical format
const fetchAndTransformData = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/goals/${CURRENT_USER_ID}`);
        if (!response.ok) throw new Error("Failed to fetch goals");
        
        const goals = await response.json();
        
        // Transform flat goals array into hierarchical structure grouped by category
        const categories = {};
        
        goals.forEach(goal => {
            // Extract category from goal_name (format: "Category: Description")
            const parts = goal.goal_name.split(": ");
            const category = parts[0] || "Other";
            const description = parts[1] || goal.goal_name;
            
            if (!categories[category]) {
                categories[category] = [];
            }
            
            categories[category].push({
                name: description,
                value: goal.target_amount
            });
        });
        
        // Build the hierarchical data structure
        const data = {
            name: "Budget",
            children: Object.entries(categories).map(([category, items]) => ({
                name: category,
                children: items
            }))
        };
        
        return data;
    } catch (error) {
        console.error("Error fetching chart data:", error);
        // Return sample data as fallback
        return {
            name: "Budget",
            children: [
                {
                    name: "Housing",
                    children: [
                        { name: "Mortgage", value: 1200 },
                        { name: "Utilities", value: 300 },
                        { name: "Insurance", value: 150 }
                    ]
                },
                {
                    name: "Lifestyle",
                    children: [
                        { name: "Groceries", value: 600 },
                        { name: "Dining", value: 200 },
                        { name: "Gym", value: 50 }
                    ]
                },
                {
                    name: "Savings",
                    children: [
                        { name: "Emergency Fund", value: 500 },
                        { name: "Vacation", value: 200 }
                    ]
                }
            ]
        };
    }
};

const drawChart = async () => {
    // 1. Clear any existing SVG before redrawing (important for resizing)
    d3.select("#sunburst").selectAll("*").remove();

    // 2. Detect container dimensions
    const container = document.getElementById("sunburst");
    const width = container.offsetWidth;
    const radius = width / 6;

    // 3. DATA: Fetch from backend
    const data = await fetchAndTransformData();

    // 4. COLOR SCALE: Teal to Pink interpolation
    const color = d3.scaleOrdinal(
        d3.quantize(d3.interpolate(d3.rgb("#008080"), d3.rgb("#ff69b4")), data.children.length + 1)
    );

    // 5. D3 PARTITION & ARC LOGIC
    const partition = data => {
        const root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);
        return d3.partition()
            .size([2 * Math.PI, root.height + 1])(root);
    };

    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
        .padRadius(radius * 1.5)
        .innerRadius(d => d.y0 * radius)
        .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

    const root = partition(data);
    root.each(d => d.current = d);

    // 6. CREATE SVG
    const svg = d3.select("#sunburst").append("svg")
        .attr("viewBox", [0, 0, width, width])
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("font", "12px sans-serif");

    const g = svg.append("g")
        .attr("transform", `translate(${width / 2},${width / 2})`);

    const path = g.append("g")
        .selectAll("path")
        .data(root.descendants().slice(1))
        .join("path")
        .attr("fill", d => { while (d.depth > 1) d = d.parent; return color(d.data.name); })
        .attr("d", d => arc(d.current));

    // 6b. ADD NAME LABELS
    g.append("g")
        .selectAll("text.label-name")
        .data(root.descendants().slice(1))
        .join("text")
        .attr("class", "label-name")
        .attr("transform", d => {
            // Calculate the angle and radius for label positioning
            const x0 = d.x0;
            const x1 = d.x1;
            const y0 = d.y0 * radius;
            const y1 = d.y1 * radius;
            
            // Position label in the middle of the arc
            const angle = (x0 + x1) / 2 - Math.PI / 2;
            const dist = (y0 + y1) / 2;
            
            return `translate(${Math.cos(angle) * dist},${Math.sin(angle) * dist})`;
        })
        .attr("text-anchor", "middle")
        .attr("dy", "-0.5em")
        .style("font-size", d => {
            // Only show labels if arc is large enough
            const arcSize = (d.y1 - d.y0) * radius;
            return Math.max(4, arcSize / 5.5) + "px";
        })
        .style("fill", d => {
            // Determine if background is light or dark
            const arcSize = (d.y1 - d.y0) * radius;
            return arcSize < 20 ? "#999" : "white"; // Gray for small segments
        })
        .style("font-weight", "600")
        .style("text-shadow", "0px 1px 2px rgba(0,0,0,0.4)")
        .style("pointer-events", "none")
        .style("display", d => {
            // Hide if too small
            const arcSize = (d.y1 - d.y0) * radius;
            return arcSize < 15 ? "none" : "block";
        })
        .text(d => d.data.name);

    // 6c. ADD AMOUNT LABELS
    g.append("g")
        .selectAll("text.label-amount")
        .data(root.descendants().slice(1))
        .join("text")
        .attr("class", "label-amount")
        .attr("transform", d => {
            // Calculate the angle and radius for label positioning
            const x0 = d.x0;
            const x1 = d.x1;
            const y0 = d.y0 * radius;
            const y1 = d.y1 * radius;
            
            // Position label in the middle of the arc
            const angle = (x0 + x1) / 2 - Math.PI / 2;
            const dist = (y0 + y1) / 2;
            
            return `translate(${Math.cos(angle) * dist},${Math.sin(angle) * dist})`;
        })
        .attr("text-anchor", "middle")
        .attr("dy", "0.8em")
        .style("font-size", d => {
            // Scale with arc size
            const arcSize = (d.y1 - d.y0) * radius;
            return Math.max(3, arcSize / 6.5) + "px";
        })
        .style("fill", d => {
            // Determine if background is light or dark
            const arcSize = (d.y1 - d.y0) * radius;
            return arcSize < 20 ? "#999" : "white";
        })
        .style("font-weight", "500")
        .style("text-shadow", "0px 1px 2px rgba(0,0,0,0.4)")
        .style("pointer-events", "none")
        .style("display", d => {
            // Hide if too small
            const arcSize = (d.y1 - d.y0) * radius;
            return arcSize < 15 ? "none" : "block";
        })
        .text(d => d.value ? `$${d.value.toLocaleString()}` : "");

    // 7. TOOLTIP & INTERACTION
    const tooltip = d3.select("#tooltip");

    path.on("mouseover", function(event, d) {
        tooltip.style("display", "block")
               .html(`<strong>${d.data.name}</strong><br>$${d.value.toLocaleString()}`);
        d3.select(this).style("opacity", 0.7);
    })
    .on("mousemove", function(event) {
        tooltip.style("left", (event.pageX + 15) + "px")
               .style("top", (event.pageY - 15) + "px");
    })
    .on("mouseout", function() {
        tooltip.style("display", "none");
        d3.select(this).style("opacity", 1);
    });

    // 8. CENTER TEXT - Display total amount spent
    const totalSpent = root.value;
    g.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "-0.2em")
        .style("font-size", `${width / 25}px`) // Scales font size with chart
        .style("fill", "var(--primary-teal)")
        .style("font-weight", "bold")
        .text(`$${totalSpent.toLocaleString()}`)
        
    // Add "Total Spent" label below the amount
    g.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "1.2em")
        .style("font-size", `${width / 40}px`)
        .style("fill", "#999")
        .style("font-weight", "500")
        .text("Total Spent");
};

// INITIALIZE: Run on load
document.addEventListener("DOMContentLoaded", drawChart);

// RESPONSIVE: Run on window resize
window.addEventListener("resize", drawChart); (debounced)
let resizeTimeout;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(drawChart, 250);
});

// REFRESH: Public function to refresh chart when data changes
window.refreshChart = async () => {
    console.log("Refreshing chart with latest data...");
    await drawChart();
    console.log("Chart refreshed!");
}