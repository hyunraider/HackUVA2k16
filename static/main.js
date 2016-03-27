$("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("active");
});

$("#eventadd").click(function(e) {
	e.preventDefault();
	$("#eventform").show();
});

$(".glyph-event").click(function(e) {
	e.preventDefault();
	$("#eventform").hide();
});

$("#assignadd").click(function(e) {
	e.preventDefault();
	$("#assignform").show();
});

$(".glyph-assign").click(function(e) {
	e.preventDefault();
	$("#assignform").hide();
});

$('#Abutton').click(function(e){
		e.preventDefault();
		console.log("starting");
		var name = $('#AinputName').val();
		var start = $('#AinputStart').val();
		var end = $('#AinputEnd').val();
		var priority = $('#Apriority').val();

		$.ajax({
			url: '/addassign',
			data: {
				name: name,
				start: start,
				end: end,
				priority: priority
			},
			type: 'POST',
			success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
          	}
	});
});

$('#Ebutton').click(function(e){
		e.preventDefault();
		console.log("starting");
		var name = $('#EinputName').val();
		var start = $('#EinputStart').val();
		var end = $('#EinputEnd').val();

		$.ajax({
			url: '/addevent',
			data: {
				name: name,
				start: start,
				end: end
			},
			type: 'POST',
			success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
          	}
	});
});
