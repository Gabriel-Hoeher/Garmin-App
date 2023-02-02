let data, subdata

window.onload = () => { 
    $.ajax({
        url: '/getData',
        type: 'POST',
        error: err => {
            console.log('ERROR:', err);
        },
        success: d => { data = d; }
    }).then(() => {
        console.log(data)
        setPage(); 
    });
}

function setPage() {
    // find all exercises
    const set = new Set();
    data.forEach(i => set.add(i.exercise))

    // create options
    const exerciseSel = $('#exercise');
    set.forEach(i => {
        let option = document.createElement('option');
        option.text = i;
        option.value = i;
        exerciseSel.append(option);
    });

    // create data for an exercise
    exerciseSel.change(() => {
        subdata = [];
        data.forEach(i => {
            if (i.exercise == exerciseSel.val()) {
                subdata.push(i);
            }
        });
        createGraph();
    });
}

function createGraph() {
    const width = 350,
    height = 150,
    margin = 5,
    padding = 5,
    adj = 30;

    if ($('div#graphs').children()[0] != null) {
        $('div#graphs').empty();
    }
    
    //create svg
    const svg = d3.select('div#graphs').append('svg')
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "-" + adj + " -" + adj + " "
    + (width + adj *3) + " " + (height + adj*3))
    .style("padding", padding)
    .style("margin", margin)
    .classed("svg-content", true);
    
    //scales
    const xScale = d3.scaleTime().range([ 0, width ]);
    const yScale = d3.scaleLinear().rangeRound([height, 0]);
    xScale.domain(d3.extent(subdata, (c) => {return c.date}));
    yScale.domain([(0), d3.max(subdata, (c) => { return c.weight; })]);
    
    //axis scale
    const yaxis = d3.axisLeft()
    .ticks(subdata.length / 4)
    .scale(yScale);
    const xaxis = d3.axisBottom()
    .ticks(subdata.length / 3)
    .scale(xScale);
    
    // svg.append("path")
    // .datum(getAverage(subdata)) //fix
    // .attr("fill", "none")
    // .attr("stroke", "red")
    // .attr("stroke-width", 1)
    // .attr("d", d3.line()
    // .x((d) => { return xScale(d.date) })
    // .y((d) => { return yScale(d.weight) })
    // )
    
    svg.append("path")
    .datum(subdata)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1)
    .attr("d", d3.line()
        .x((d) => { return xScale(d.date) })
        .y((d) => { return yScale(d.weight) })
    )
    
    svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xaxis);
    svg.append("g").attr("class", "axis").call(yaxis);
}

function getAverage(subData) {
    return 1;
}