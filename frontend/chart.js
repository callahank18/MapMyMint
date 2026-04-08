/**
 * MapMyMint - D3 Sunburst Logic
 * Responsive, Hierarchical Budget Visualization
 */

const drawChart = () => {
    // 1. Clear any existing SVG before redrawing (important for resizing)
    d3.select("#sunburst").selectAll("*").remove();

    // 2. Detect container dimensions
    const container = document.getElementById("sunburst");
    const width = container.offsetWidth;
    const radius = width / 6;

    // 3. DATA: Sample hierarchy (Replace with your local DB/CSV fetch later)
    const data = {
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

    // 8. CENTER TEXT
    g.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "0.35em")
        .style("font-size", `${width / 25}px`) // Scales font size with chart
        .style("fill", "#666")
        .style("font-weight", "bold")
        .text("Total Map");
};

// INITIALIZE: Run on load
document.addEventListener("DOMContentLoaded", drawChart);

// RESPONSIVE: Run on window resize
window.addEventListener("resize", drawChart);