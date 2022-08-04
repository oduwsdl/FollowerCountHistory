const path_colors = ["#FF6961",
					"#FFB480",
					"#F8F38D",
					"#42D6A4",
					"#08CAD1",
					"#59ADF6",
					"#9D94FF",
					"#C780E8",
					"#8A3F64",
					"#4F2E39"];

var handles = [];
var current_gid = 0;

const graphID = {
	FOLLOWER_COUNT : 0,
	FOLLOWER_GROWTH : 1,
	FOLLOWER_RATE : 2
}

generateGraph();

function generateGraph(graph_id = current_gid) {
	console.log("graph generating...");
	current_gid = graph_id;

	let formatTime = d3.timeParse("%Y%m%d%H%M%S");
	var activePlots;

	var min_x = 0;
	var max_x = 0;
	var min_y = 0;
	var max_y = 0;
	var tempTime;

	var margin;
	var svg;
	var x;
	var y;
	var mouseG;
	var mousePerLine;
	var lines;

	var g_holder = document.getElementById("graph_holder");
	if(g_holder != null)
	{
		g_holder.remove();
	}

	var g_title = document.getElementById("graph__title");

	switch (current_gid) {
		case graphID.FOLLOWER_COUNT:
			g_title.innerHTML = "Twitter Follower Growth Over Time";
			break;
		case graphID.FOLLOWER_GROWTH:
			g_title.innerHTML = "Absolute and Percentage Follower Growth Over Time w.r.t. First Memento";
			break;
		case graphID.FOLLOWER_RATE:
			g_title.innerHTML = "New Followers Increase Over Time w.r.t. First Memento";
			break;
	}

	switch (current_gid) {
		case graphID.FOLLOWER_COUNT:
			formatTime = d3.timeParse("%Y%m%d%H%M%S");
			activePlots = mementoData.filter(function(plot) {
				return plot.active;
			});
	
			min_x = 100000000000000;
			max_x = 0;
			min_y = 100000000000000;
			max_y = 0;
			activePlots.forEach(function(ap) {
				ap.data.forEach(function(d) {
					tempTime = new Date(formatTime(d.MementoDatetime));
					if(min_x > tempTime.getTime()) {
						min_x = tempTime.getTime();
					} 

					if(max_x < tempTime.getTime()) {
						max_x = tempTime.getTime();
					}

					if(min_y > parseInt(d.FollowerCount)) {
						min_y = parseInt(d.FollowerCount);
					} 

					if(max_y < parseInt(d.FollowerCount)) {
						max_y = parseInt(d.FollowerCount);
					} 
				});
			});

			margin = {top : 10, right : 30, bottom : 30, left: 60},
				width = 937 - margin.left - margin.right,
				height = 562 - margin.top - margin.bottom;

			svg = d3.select("#container__graph")
				.append("svg")
				.attr('id', "graph_holder")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", `translate(${margin.left},${margin.top})`)
				.style("fill", "#71767A");
	
			//x-axis
			x = d3.scaleTime()
				.domain([min_x, max_x])
				.range([ 0, width ]);
			svg.append("g")
				.attr("transform", `translate(0, ${height})`)
				.attr("class", "x axis")
				.call(d3.axisBottom(x));

			//y-axis
			y = d3.scaleLinear()
				.domain([min_y, max_y])
				.range([ height, 0 ]);
			svg.append("g")
				.attr("class", "y axis")
				.call(d3.axisLeft(y));

			//x-axis label
			svg.append("text")
				.attr("text-anchor", "end")
				.attr("font-size", "12px")
				.style("stroke", "#1d9bf0")
				.attr("x", width / 2)
				.attr("y", height + margin.top + 18)
				.text("Date");

			//y-axis label
			svg.append("text")
				.attr("text-anchor", "middle")
				.attr("font-size", "12px")
				.attr("transform", "rotate(-90)")
				.style("stroke", "#1d9bf0")
				.attr("x", -height/2 + margin.top)
				.attr("y", -margin.left + 10)
				.text("Follower Count");

			mouseG = svg.append("g")
				.attr("id", "mouse-over-effects")
				.attr("class", "mouse-over-effects");

			mouseG.append("path")
				.attr("class", "mouse-line")
				.style("stroke", "#71767A")
				.style("stroke-width", "1.5px")
				.style("opacity", "0");

			for(var i = 0; i < activePlots.length; i++) 
			{
				svg.append("path")
					.datum(activePlots[i].data.filter(function(d) {
						return Number.isInteger(parseInt(d.FollowerCount));
					}))
					.attr("class", "line")
					.attr("fill", "none")
					.attr("stroke", path_colors[activePlots[i].id%10])
					.attr("stroke-width", 1.5)
					.attr("d", d3.line()
						.x(function(d) { return x(formatTime(d.MementoDatetime)) })
						.y(function(d) { return y(parseInt(d.FollowerCount)) })
					);

				mousePerLine = mouseG.append("g")
					.attr("class", "mouse-per-line")
					.datum(activePlots[i].data.filter(function(d) {
						return Number.isInteger(parseInt(d.FollowerCount));
					}));

				mousePerLine.append("circle")
					.attr("r", 7)
					.style("stroke", path_colors[activePlots[i].id%10])
					.style("fill", "none")
					.style("stroke-width", "1px")
					.style("opacity", "0");

				mousePerLine.append("text")
					.style("stroke", path_colors[activePlots[i].id%10])
					.attr("transform", "translate(10,-15)");

				handles.push(activePlots[i].handle);
			}

			lines = document.getElementsByClassName('line');

			mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
				.attr('width', width) // can't catch mouse events on a g element
				.attr('height', height)
				.attr('fill', 'none')
				.attr('pointer-events', 'all')
				.on('mouseout', function() { // on mouse out hide line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "0");
				})
				.on('mouseover', function() { // on mouse in show line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "1");
				})
				.on('mousemove', function() { // mouse moving over canvas
					var mouse = d3.mouse(this);
					d3.select(".mouse-line")
						.attr("d", function() {
							var d = "M" + mouse[0] + "," + height;
							d += " " + mouse[0] + "," + 0;
							return d;
					});

					d3.selectAll(".mouse-per-line")
						.attr("transform", function(d, i) {
							var beginning = 0,
							end = lines[i].getTotalLength(),
							target = null;
							//console.log(end);
							while (true){
								target = Math.floor((beginning + end) / 2);
								pos = lines[i].getPointAtLength(target);
								if ((target === end || target === beginning) && pos.x !== mouse[0]) {
									break;
								}
								if (pos.x > mouse[0])      end = target;
								else if (pos.x < mouse[0]) beginning = target;
								else break; //position found
							}
							let reformatTime = d3.timeFormat("%B %d, %Y");

							var hoveredTime = reformatTime(x.invert(pos.x));
							
							d3.select(this).select('text')
								.text("@" + handles[i] + ": " + hoveredTime+", "+y.invert(pos.y).toFixed(0));
				
							if (mouse[0] > width/2) {
								d3.select(this).select('text')
									.attr("transform", "translate(-10,25)")
									.attr("text-anchor", "end");
							} else {
								d3.select(this).select('text')
									.attr("transform", "translate(10,-15)")
									.attr("text-anchor", "start");
							}
							return "translate(" + mouse[0] + "," + pos.y +")";
						})
						.attr("opacity", function(d, i) {
							var box = lines[i].getBoundingClientRect();
							var root = document.getElementById('mouse-over-effects').getBoundingClientRect();

							if(mouse[0] < box.left-root.left || mouse[0] > box.right-root.left) {
								return "0";
							} else {
								return "1";
							}
						});
			  });
			break;
		case graphID.FOLLOWER_GROWTH:
			formatTime = d3.timeParse("%Y%m%d%H%M%S");
			activePlots = mementoData.filter(function(plot) {
				return plot.active;
			});
	
			min_x = 100000000000000;
			max_x = 0;
			min_y = 100000000000000;
			max_y = 0;
			activePlots.forEach(function(ap) {
				ap.data.forEach(function(d) {
					tempTime = new Date(formatTime(d.MementoDatetime));
					if(min_x > tempTime.getTime()) {
						min_x = tempTime.getTime();
					} 

					if(max_x < tempTime.getTime()) {
						max_x = tempTime.getTime();
					}

					if(min_y > Number(d.AbsFolRate)) {
						min_y = Number(d.AbsFolRate);
					} 

					if(max_y < Number(d.AbsFolRate)) {
						max_y = Number(d.AbsFolRate);
					} 
				});
			});

			margin = {top : 10, right : 30, bottom : 30, left: 60},
				width = 937 - margin.left - margin.right,
				height = 562 - margin.top - margin.bottom;

			svg = d3.select("#container__graph")
				.append("svg")
				.attr('id', "graph_holder")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", `translate(${margin.left},${margin.top})`)
				.style("fill", "#71767A");
	
			//x-axis
			x = d3.scaleTime()
				.domain([min_x, max_x])
				.range([ 0, width ]);
			svg.append("g")
				.attr("transform", `translate(0, ${height})`)
				.attr("class", "x axis")
				.call(d3.axisBottom(x));

			//y-axis
			y = d3.scaleLinear()
				.domain([min_y, max_y])
				.range([ height, 0 ]);
			svg.append("g")
				.attr("class", "y axis")
				.call(d3.axisLeft(y));

			//x-axis label
			svg.append("text")
				.attr("text-anchor", "end")
				.attr("font-size", "12px")
				.style("stroke", "#1d9bf0")
				.attr("x", width / 2)
				.attr("y", height + margin.top + 18)
				.text("Date");

			//y-axis label
			svg.append("text")
				.attr("text-anchor", "middle")
				.attr("font-size", "12px")
				.attr("transform", "rotate(-90)")
				.style("stroke", "#1d9bf0")
				.attr("x", -height/2 + margin.top)
				.attr("y", -margin.left + 10)
				.text("Increase of New Followers in a Day");

			mouseG = svg.append("g")
				.attr("id", "mouse-over-effects")
				.attr("class", "mouse-over-effects");

			mouseG.append("path")
				.attr("class", "mouse-line")
				.style("stroke", "#71767A")
				.style("stroke-width", "1.5px")
				.style("opacity", "0");

			for(var i = 0; i < activePlots.length; i++) 
			{
				svg.append("path")
					.datum(activePlots[i].data.filter(function(d) {
						return Number(d.AbsFolRate);
					}))
					.attr("class", "line")
					.attr("fill", "none")
					.attr("stroke", path_colors[activePlots[i].id%10])
					.attr("stroke-width", 1.5)
					.attr("d", d3.line()
						.x(function(d) { return x(formatTime(d.MementoDatetime)) })
						.y(function(d) { return y(Number(d.AbsFolRate)) })
					);

				var mousePerLine = mouseG.append("g")
					.attr("class", "mouse-per-line")
					.datum(activePlots[i].data.filter(function(d) {
						return Number(d.AbsFolRate);
					}));

				mousePerLine.append("circle")
					.attr("r", 7)
					.style("stroke", path_colors[activePlots[i].id%10])
					.style("fill", "none")
					.style("stroke-width", "1px")
					.style("opacity", "0");

				mousePerLine.append("text")
					.style("stroke", path_colors[activePlots[i].id%10])
					.attr("transform", "translate(10,-15)");

				handles.push(activePlots[i].handle);
			}

			lines = document.getElementsByClassName('line');

			mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
				.attr('width', width) // can't catch mouse events on a g element
				.attr('height', height)
				.attr('fill', 'none')
				.attr('pointer-events', 'all')
				.on('mouseout', function() { // on mouse out hide line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "0");
				})
				.on('mouseover', function() { // on mouse in show line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "1");
				})
				.on('mousemove', function() { // mouse moving over canvas
					var mouse = d3.mouse(this);
					d3.select(".mouse-line")
						.attr("d", function() {
							var d = "M" + mouse[0] + "," + height;
							d += " " + mouse[0] + "," + 0;
							return d;
					});

					d3.selectAll(".mouse-per-line")
						.attr("transform", function(d, i) {
							var beginning = 0,
							end = lines[i].getTotalLength(),
							target = null;
							//console.log(end);
							while (true){
								target = Math.floor((beginning + end) / 2);
								pos = lines[i].getPointAtLength(target);
								if ((target === end || target === beginning) && pos.x !== mouse[0]) {
									break;
								}
								if (pos.x > mouse[0])      end = target;
								else if (pos.x < mouse[0]) beginning = target;
								else break; //position found
							}
							let reformatTime = d3.timeFormat("%B %d, %Y");

							var hoveredTime = reformatTime(x.invert(pos.x));

							d3.select(this).select('text')
								.text("@" + handles[i] + ":\n" + hoveredTime+", "+y.invert(pos.y).toFixed(5));
				
							if (mouse[0] > width/2) {
								d3.select(this).select('text')
									.attr("transform", "translate(-10,25)")
									.attr("text-anchor", "end");
							} else {
								d3.select(this).select('text')
									.attr("transform", "translate(10,-15)")
									.attr("text-anchor", "start");
							}
							return "translate(" + mouse[0] + "," + pos.y +")";
						})
						.attr("opacity", function(d, i) {
							var box = lines[i].getBoundingClientRect();
							var root = document.getElementById('mouse-over-effects').getBoundingClientRect();

							if(mouse[0] < box.left-root.left || mouse[0] > box.right-root.left) {
								return "0";
							} else {
								return "1";
							}
						});
			  });
			break;
		case graphID.FOLLOWER_RATE:
			formatTime = d3.timeParse("%Y%m%d%H%M%S");
			activePlots = mementoData.filter(function(plot) {
				return plot.active;
			});
	
			min_x = 100000000000000;
			max_x = 0;
			min_y = 100000000000000;
			max_y = 0;
			activePlots.forEach(function(ap) {
				ap.data.forEach(function(d) {
					tempTime = new Date(formatTime(d.MementoDatetime));
					if(min_x > tempTime.getTime()) {
						min_x = tempTime.getTime();
					} 

					if(max_x < tempTime.getTime()) {
						max_x = tempTime.getTime();
					}

					if(min_y > Number(d.AbsGrowth)) {
						min_y = Number(d.AbsGrowth);
					} 

					if(max_y < Number(d.AbsGrowth)) {
						max_y = Number(d.AbsGrowth);
					} 
				});
			});

			margin = {top : 10, right : 30, bottom : 30, left: 60},
				width = 937 - margin.left - margin.right,
				height = 562 - margin.top - margin.bottom;

			svg = d3.select("#container__graph")
				.append("svg")
				.attr('id', "graph_holder")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", `translate(${margin.left},${margin.top})`)
				.style("fill", "#71767A");
	
			//x-axis
			x = d3.scaleTime()
				.domain([min_x, max_x])
				.range([ 0, width ]);
			svg.append("g")
				.attr("transform", `translate(0, ${height})`)
				.attr("class", "x axis")
				.call(d3.axisBottom(x));

			//y-axis
			y = d3.scaleLinear()
				.domain([min_y, max_y])
				.range([ height, 0 ]);
			svg.append("g")
				.attr("class", "y axis")
				.call(d3.axisLeft(y));

			//x-axis label
			svg.append("text")
				.attr("text-anchor", "end")
				.attr("font-size", "12px")
				.style("stroke", "#1d9bf0")
				.attr("x", width / 2)
				.attr("y", height + margin.top + 18)
				.text("Date");

			//y-axis label
			svg.append("text")
				.attr("text-anchor", "middle")
				.attr("font-size", "12px")
				.attr("transform", "rotate(-90)")
				.style("stroke", "#1d9bf0")
				.attr("x", -height/2 + margin.top)
				.attr("y", -margin.left + 10)
				.text("Increase in Follower Count");

			mouseG = svg.append("g")
				.attr("id", "mouse-over-effects")
				.attr("class", "mouse-over-effects");

			mouseG.append("path")
				.attr("class", "mouse-line")
				.style("stroke", "#71767A")
				.style("stroke-width", "1.5px")
				.style("opacity", "0");

			for(var i = 0; i < activePlots.length; i++) 
			{
				svg.append("path")
					.datum(activePlots[i].data.filter(function(d) {
						return Number(d.AbsGrowth);
					}))
					.attr("class", "line")
					.attr("fill", "none")
					.attr("stroke", path_colors[activePlots[i].id%10])
					.attr("stroke-width", 1.5)
					.attr("d", d3.line()
						.x(function(d) { return x(formatTime(d.MementoDatetime)) })
						.y(function(d) { return y(Number(d.AbsGrowth)) })
					);

				var mousePerLine = mouseG.append("g")
					.attr("class", "mouse-per-line")
					.datum(activePlots[i].data.filter(function(d) {
						return Number(d.AbsGrowth);
					}));

				mousePerLine.append("circle")
					.attr("r", 7)
					.style("stroke", path_colors[activePlots[i].id%10])
					.style("fill", "none")
					.style("stroke-width", "1px")
					.style("opacity", "0");

				mousePerLine.append("text")
					.style("stroke", path_colors[activePlots[i].id%10])
					.attr("transform", "translate(10,-15)");

				handles.push(activePlots[i].handle);
			}

			lines = document.getElementsByClassName('line');

			mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
				.attr('width', width) // can't catch mouse events on a g element
				.attr('height', height)
				.attr('fill', 'none')
				.attr('pointer-events', 'all')
				.on('mouseout', function() { // on mouse out hide line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "0");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "0");
				})
				.on('mouseover', function() { // on mouse in show line, circles and text
					d3.select(".mouse-line")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line circle")
						.style("opacity", "1");
					d3.selectAll(".mouse-per-line text")
						.style("opacity", "1");
				})
				.on('mousemove', function() { // mouse moving over canvas
					var mouse = d3.mouse(this);
					d3.select(".mouse-line")
						.attr("d", function() {
							var d = "M" + mouse[0] + "," + height;
							d += " " + mouse[0] + "," + 0;
							return d;
					});

					d3.selectAll(".mouse-per-line")
						.attr("transform", function(d, i) {
							var beginning = 0,
							end = lines[i].getTotalLength(),
							target = null;
							//console.log(end);
							while (true){
								target = Math.floor((beginning + end) / 2);
								pos = lines[i].getPointAtLength(target);
								if ((target === end || target === beginning) && pos.x !== mouse[0]) {
									break;
								}
								if (pos.x > mouse[0])      end = target;
								else if (pos.x < mouse[0]) beginning = target;
								else break; //position found
							}
							let reformatTime = d3.timeFormat("%B %d, %Y");

							var hoveredTime = reformatTime(x.invert(pos.x));

							d3.select(this).select('text')
								.text("@" + handles[i] + ":\n" + hoveredTime+", "+y.invert(pos.y).toFixed(5));
				
							if (mouse[0] > width/2) {
								d3.select(this).select('text')
									.attr("transform", "translate(-10,25)")
									.attr("text-anchor", "end");
							} else {
								d3.select(this).select('text')
									.attr("transform", "translate(10,-15)")
									.attr("text-anchor", "start");
							}
							return "translate(" + mouse[0] + "," + pos.y +")";
						})
						.attr("opacity", function(d, i) {
							var box = lines[i].getBoundingClientRect();
							var root = document.getElementById('mouse-over-effects').getBoundingClientRect();

							if(mouse[0] < box.left-root.left || mouse[0] > box.right-root.left) {
								return "0";
							} else {
								return "1";
							}
						});
			  });
			break;

	}
}

function hideLine(e) {
	var id = e.parentNode.id;
	const index = mementoData.findIndex((item) => {
		return item.id === id;
	});

	mementoData[index].active = !mementoData[index].active;
	generateGraph();
}

function hideAdditionalFeatures(e) {
	var id = e.parentNode.id;
	var af_div = e.parentNode.querySelector('.handle__additional__features');

	if(af_div.style.display == 'none') {
		af_div.style.display = 'inline-flex';
	} else {
		af_div.style.display = 'none';
	}
}

window.onload = generateGraph(0);
</script>