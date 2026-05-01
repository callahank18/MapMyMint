/**
 * MapMyMint - D3 Sunburst Logic
 */

const CURRENT_USER_ID = localStorage.getItem("currentUserId") || 1;
let observerReady = false;
let resizeTimeout;
window.isDrawing = false;

/**
 * 1. DATA TRANSFORMATION
 */
const fetchAndTransformData = async () => {
    try {
        const [catRes, txRes, goalRes] = await Promise.all([
            fetch(`http://127.0.0.1:8000/categories/${CURRENT_USER_ID}`),
            fetch(`http://127.0.0.1:8000/transactions/${CURRENT_USER_ID}`),
            fetch(`http://127.0.0.1:8000/goals/${CURRENT_USER_ID}`)
        ]);

        const categories = await catRes.json();
        const transactions = await txRes.json();
        const goals = await goalRes.json();

        let grandTotalSpent = 0;
        let totalSavingsProgress = 0;
        let grandTotalTarget = 0;

        const spendingChildren = categories.map(cat => {
            const catTxs = transactions.filter(tx =>
                (tx.category_id && tx.category_id === cat.id) ||
                (tx.category_name && tx.category_name.toLowerCase() === cat.name.toLowerCase())
            );

            const totalSpent = catTxs.reduce((sum, tx) => sum + tx.amount, 0);
            const limit = cat.limit_amount || 0;
            grandTotalSpent += totalSpent;
            grandTotalTarget += limit;

            let children = catTxs.map(tx => ({
                name: tx.description,
                value: tx.amount,
                type: 'transaction',
                isOver: limit > 0 && totalSpent > limit
            }));

            if (limit > 0 && totalSpent < limit) {
                children.push({ name: "Remaining", value: limit - totalSpent, type: 'buffer' });
            }

            if (children.length === 0) {
                children.push({ name: "No Data", value: 1, type: 'empty' });
            }

            return { name: cat.name, children, isOver: limit > 0 && totalSpent > limit };
        });

        const savingsChildren = goals.map(goal => {
            const progress = goal.current_amount || 0;
            const target = goal.target_amount || 0;
            totalSavingsProgress += progress;
            grandTotalTarget += target;

            let children = [];
            if (progress > 0) children.push({ name: "Saved", value: progress, type: 'transaction' });
            if (target > progress) children.push({ name: "To Go", value: target - progress, type: 'buffer' });
            if (children.length === 0) children.push({ name: "No Data", value: 1, type: 'empty' });

            return { name: goal.goal_name, children };
        });

        return {
            hierarchy: {
                name: "Budget",
                children: [
                    { name: "Spending", children: spendingChildren },
                    { name: "Savings",  children: savingsChildren  }
                ]
            },
            meta: {
                totalSpent: grandTotalSpent + totalSavingsProgress,
                totalTarget: grandTotalTarget,
                uniqueCount: categories.length + goals.length
            }
        };
    } catch (error) {
        console.error("Data Transformation Error:", error);
        return { hierarchy: { name: "Error", children: [] }, meta: { totalSpent: 0, totalTarget: 0, uniqueCount: 5 } };
    }
};

/**
 * 2. THEME UTILITY
 */
const getThemeColors = () => {
    const s = getComputedStyle(document.documentElement);
    return {
        spendingColor: s.getPropertyValue('--chart-spending').trim() || '#008080',
        savingsColor:  s.getPropertyValue('--chart-savings').trim() || '#ff69b4',
        start: s.getPropertyValue('--chart-start').trim() || '#008080',
        end: s.getPropertyValue('--chart-end').trim() || '#ff69b4',
        bufferOpacity: parseFloat(s.getPropertyValue('--chart-buffer').trim()) || 0.3,
        warning: s.getPropertyValue('--chart-warning').trim() || 'crimson',
        textPrimary: s.getPropertyValue('--text-primary').trim() || '#1a1a1a',
        textSecondary: s.getPropertyValue('--text-secondary').trim() || '#555555'
    };
};

/**
 * 3. CORE DRAWING FUNCTION
 */
const drawChart = async () => {
    const container = document.getElementById("sunburst");
    if (!container) return;

    if (window.isDrawing) return;
    window.isDrawing = true;

    try {
        console.trace("drawChart execution started");
        
        // FIXED: Added parentheses to actually call the function
        d3.select("#sunburst").selectAll("*").remove(); 

        const width = container.offsetWidth;
        const radius = width / 6;

        const { hierarchy, meta } = await fetchAndTransformData();
        const theme = getThemeColors();

        const color = d3.scaleOrdinal(
            d3.quantize(
                d3.interpolateRgb(theme.start, theme.end),
                Math.max(meta.uniqueCount + 2, 4)
            )
        );

        const partition = data => {
            const root = d3.hierarchy(data)
                .sum(d => d.value)
                .sort((a, b) => b.value - a.value);
            return d3.partition().size([2 * Math.PI, root.height + 1])(root);
        };

        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

        const root = partition(hierarchy);
        root.each(d => d.current = d);

        const svg = d3.select("#sunburst").append("svg")
            .attr("viewBox", [0, 0, width, width])
            .attr("preserveAspectRatio", "xMidYMid meet")
            .style("font", "12px sans-serif");

        const g = svg.append("g")
            .attr("transform", `translate(${width / 2},${width / 2})`);

        const getFill = d => {
            if (d.depth === 1) {
                return d.data.name === "Savings" ? theme.savingsColor : theme.spendingColor;
            }
            let colorNode = d;
            while (colorNode.depth > 2) colorNode = colorNode.parent;
            const baseColor = d3.color(color(colorNode.data.name));
            if (d.data.type === 'buffer' || d.data.type === 'empty') {
                baseColor.opacity = theme.bufferOpacity;
                return baseColor.toString();
            }
            if (d.data.isOver || (d.parent && d.parent.data.isOver)) {
                return d3.interpolateRgb(baseColor.toString(), theme.warning)(0.4);
            }
            return baseColor.toString();
        };

        const tooltip = d3.select("#tooltip");

        g.append("g")
            .selectAll("path")
            .data(root.descendants().slice(1))
            .join("path")
            .attr("fill", d => getFill(d))
            .attr("d", d => arc(d.current))
            .on("mouseover", function(event, d) {
                d3.select(this).style("opacity", 0.75);
                const parentLabel = d.depth > 2 ? `<span style="opacity:0.7">${d.parent.data.name} › </span>` : "";
                tooltip.style("display", "block").html(`${parentLabel}<strong>${d.data.name}</strong><br>$${d.value.toLocaleString()}`);
            })
            .on("mousemove", event => {
                tooltip.style("left", (event.pageX + 15) + "px").style("top", (event.pageY - 15) + "px");
            })
            .on("mouseout", function() {
                d3.select(this).style("opacity", 1);
                tooltip.style("display", "none");
            });

        const labelArcSize = d => (d.y1 - d.y0) * radius;
        const labelAngle = d => ((d.x0 + d.x1) / 2) * 180 / Math.PI - 90;
        const labelDist = d => (d.y0 + d.y1) / 2 * radius;

        g.append("g")
            .attr("pointer-events", "none")
            .selectAll("text.label-name")
            .data(root.descendants().slice(1).filter(d => {
                const arcPx = labelArcSize(d);
                return arcPx >= 14 && (d.x1 - d.x0) > 0.12;
            }))
            .join("text")
            .attr("class", "label-name")
            .attr("transform", d => {
                const angle = labelAngle(d);
                const dist = labelDist(d);
                return `rotate(${angle}) translate(${dist},0) rotate(${angle > 90 ? 180 : 0})`;
            })
            .attr("text-anchor", "middle")
            .attr("dy", d => d.depth >= 3 ? "-0.4em" : "0.35em")
            .style("font-size", d => Math.min(12, Math.max(7, labelArcSize(d) / 5)) + "px")
            .style("font-weight", "600")
            .style("fill", theme.textPrimary)
            .style("text-shadow", "0 1px 2px rgba(0,0,0,0.35)")
            .text(d => d.data.name);
        
        g.append("g")
            .attr("pointer-events", "none")
            .selectAll("text.label-amount")
            .data(root.descendants().slice(1).filter(d => {
                const arcPx = labelArcSize(d);
                return d.depth >= 3 && arcPx >= 18 && (d.x1 - d.x0) > 0.14;
            }))
            .join("text")
            .attr("class", "label-amount")
            .attr("transform", d => {
                const angle = labelAngle(d);
                const dist = labelDist(d);
                return `rotate(${angle}) translate(${dist},0) rotate(${angle > 90 ? 180 : 0})`;
            })
            .attr("text-anchor", "middle")
            .attr("dy", "0.75em")
            .style("font-size", d => Math.min(10, Math.max(6, labelArcSize(d) / 6.5)) + "px")
            .style("font-weight", "400")
            .style("fill", theme.textSecondary)
            .style("text-shadow", "0 1px 2px rgba(0,0,0,0.35)")
            .text(d => d.value ? `$${d.value.toLocaleString()}` : "");

        const centerGroup = g.append("g").attr("class", "center-text");
        centerGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "-0.3em")
            .style("font-size", `${width / 20}px`)
            .style("fill", theme.start)
            .style("font-weight", "bold")
            .text(`$${meta.totalSpent.toLocaleString()}`);

        centerGroup.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "1.2em")
            .style("font-size", `${width / 45}px`)
            .style("fill", theme.textSecondary)
            .text(`of $${meta.totalTarget.toLocaleString()} Plan`);

        console.log("Chart successfully rendered.");
    } catch (error) {
        console.error("Chart Render Failure:", error);
    } finally {
        window.isDrawing = false;
    }
};

/**
 * 4. INITIALIZATION & OBSERVERS
 */

// Handle Window Resize (Debounced)
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(drawChart, 250);
});

// Single Point of Entry for DOM Load
document.addEventListener("DOMContentLoaded", async () => {
    console.log("DOMContentLoaded: Initializing Sunburst...");
    await drawChart();
    setTimeout(() => { 
        observerReady = true; 
        console.log("Theme Observer Armed.");
    }, 500);
});

// Watch for Theme Changes
const themeObserver = new MutationObserver(() => {
    if (observerReady) {
        console.log("Theme mutation detected.");
        drawChart();
    }
});

themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
});

window.refreshChart = async () => { 
    console.log("External refresh requested...");
    await drawChart(); 
};