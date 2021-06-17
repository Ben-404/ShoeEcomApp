var data = {
    labels: ['Nike', 'adidas', 'Converse', 'Vans'],
    series: [pc_brand[0], pc_brand[1], pc_brand[2], pc_brand[3]]
};

alert(data["series"])

new Chartist.Bar('#brand1', data);