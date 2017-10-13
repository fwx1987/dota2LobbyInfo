

var lineFormatter = function(cell, formatterParams){
    setTimeout(function(){ //give cell enough time to be added to the DOM before calling sparkline formatter
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"line", disableTooltips:true});
    }, 10);
};

//generate bar chart
var barFormatter = function(cell, formatterParams){
    setTimeout(function(){ //give cell enough time to be added to the DOM before calling sparkline formatter
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"bar", barWidth:14, disableTooltips:true});
    }, 10);
};

//generate discrete chart
var tristateFormatter = function(cell, formatterParams){
    setTimeout(function(){ //give cell enough time to be added to the DOM before calling sparkline formatter
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"tristate", barWidth:14, disableTooltips:true});
    }, 10);
};


//generate box plot
var boxFormatter = function(cell, formatterParams){
    setTimeout(function(){ //give cell enough time to be added to the DOM before calling sparkline formatter
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"box", disableTooltips:false,minValue:200,maxValue:800});
    }, 10);
};


//generate Pie chart
var pieFormatter = function(cell, formatterParams){
    setTimeout(function(){ //give cell enough time to be added to the DOM before calling sparkline formatter
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"pie", disableTooltips:true});
    }, 10);
};


$("#radiant-table").tabulator({
    //width:216,
	//height:205, // set height of table, this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitDataFill",
	//layout:"fitColumns",
	//height:450,
	//responsiveLayout:true,
	//fitColumns:true, //fit columns to width of table (optional)
	//groupBy:"type",
	//groupToggleElement:"header",
	//groupStartOpen:false,

    columns:[ //Define Table Columns
			{title:"Lobby", field:"player_slot",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if(value.indexOf("hero_") != -1){
						return "";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return value;
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
				}},

			{field:"account_avatar",width:125,formatter:function(cell, formatterParams){
				   var value = cell.getValue();
				   
				   if (value != null)
				   {
					if(value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
					}
				}},
			{title:"Player/Hero", width:150,field:"account_name"},
			{title:"Games", field:"total_games"},
			{title:"Match History", field:"win_history",width:160, formatter:tristateFormatter},

			{title:"Avg GPM", field:"total_avg_gpm"},
			{title:"GPM Box Plot", field:"gpm_history",width:160, formatter:boxFormatter },
			{title:"Win Avg GPM", field:"total_avg_win_gpm"},
			{title:"Lose Avg GPM", field:"total_avg_lose_gpm"},


			{title:"Favourite Hero", width:68,field:"hero_sb_image",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
				    if ("undefined"  != typeof value) {
						if (value !=null)
					{
					if (value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}



					}}

				}},
			{title:"Games", field:"hero_games_played"},
			{title:"Fav Win History", field:"hero_win_history",formatter:tristateFormatter},
			{title:"Fav Win GPM", field:"hero_gpm_for_win"},
			{title:"Fav Lose GPM", field:"hero_gpm_for_lose"}

		//{title:"day reocrd", field:"hero_last_24_hrs_win_rate",formatter:"progress",formatterParams:{min:10,max:80,color:"#FF0000"}},
		//{title:"day win", field:"hero_last_24_hrs_win"},
    ],

	rowFormatter:function(row){
        //row - row component

        var data = row.getData();


		if (data.player_slot !=null){

			if (data.player_slot.length ==1)
			{
				row.getElement().addClass("player_row")
				row.getElement().css({"height":"50px"});
			}

			if (data.player_slot.indexOf("hero_")!=-1)
			//if (data != null and data.type.indexOf("hero_")!=-1)
			{
				row.getElement().css({"background-color":"#A6A6DF"});
				row.getElement().css({"height":"50px"});
				//row.getElement().style.display= 'none';
				//row.getElement().hide();
				//alert(row.getElement().getAttribute( "class" ))

				var s = row.getElement()[0];

				s.classList.add("hero_row");
				s.classList.add(data.player_slot);
				//s.style.display = 'None';
				s.hidden = false
				//alert(1);

			}


		}



    },



	rowClick:function(e, row){ //trigger an alert message when the row is clicked
        //alert("Row " + row.getData().player_slot + " Clicked!!!!");
		var rowHero = document.getElementsByClassName('hero_'+(row.getData().player_slot))
		for (i=0;i<rowHero.length;i++)
		{
			if (rowHero[i].hidden )
			{
				rowHero[i].hidden = false
			}else
			{
				rowHero[i].hidden=true
			}
		//rowHero[i].hidden = true
		}


    },


});

$("#dire-table").tabulator({
    //width:216,
	//height:205, // set height of table, this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitDataFill",
	//layout:"fitColumns",
	//height:450,
	//responsiveLayout:true,
	//fitColumns:true, //fit columns to width of table (optional)
	//groupBy:"type",
	//groupToggleElement:"header",
	//groupStartOpen:false,

    columns:[ //Define Table Columns
			{title:"Lobby", field:"player_slot",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if(value.indexOf("hero_") != -1){
						return "";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return value;
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
				}},

			{field:"account_avatar",width:125,formatter:function(cell, formatterParams){
				   var value = cell.getValue();
				   					if (value !=null)
					{
					if(value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
					}
				}},
			{title:"Player/Hero", width:150,field:"account_name"},
			{title:"Games", field:"total_games"},
			{title:"Win History", field:"win_history",width:160, formatter:tristateFormatter},

			{title:"Avg GPM", field:"total_avg_gpm"},
			{title:"GPM Box Plot", field:"gpm_history",width:160, formatter:boxFormatter },
			{title:"Win Avg GPM", field:"total_avg_win_gpm"},
			{title:"Lose Avg GPM", field:"total_avg_lose_gpm"},


			{title:"Favourite Hero", width:68,field:"hero_sb_image",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
				    if ("undefined"  != typeof value) {
					if (value !=null)
					{
					if (value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}



					}}

				}},
			{title:"Games", field:"hero_games_played"},
			{title:"Fav Win History", field:"hero_win_history",formatter:tristateFormatter},
			{title:"Fav Win GPM", field:"hero_gpm_for_win"},
			{title:"Fav Lose GPM", field:"hero_gpm_for_lose"}

		//{title:"day reocrd", field:"hero_last_24_hrs_win_rate",formatter:"progress",formatterParams:{min:10,max:80,color:"#FF0000"}},
		//{title:"day win", field:"hero_last_24_hrs_win"},
    ],

	rowFormatter:function(row){
        //row - row component

        var data = row.getData();


		if (data.player_slot !=null){

			if (data.player_slot.length ==1)
			{
				row.getElement().addClass("player_row")
				row.getElement().css({"height":"50px"});
			}

			if (data.player_slot.indexOf("hero_")!=-1)
			//if (data != null and data.type.indexOf("hero_")!=-1)
			{
				row.getElement().css({"background-color":"#A6A6DF"});
				row.getElement().css({"height":"50px"});
				//row.getElement().style.display= 'none';
				//row.getElement().hide();
				//alert(row.getElement().getAttribute( "class" ))

				var s = row.getElement()[0];

				s.classList.add("hero_row");
				s.classList.add(data.player_slot);
				//s.style.display = 'None';
				s.hidden = false
				//alert(1);

			}


		}



    },



	rowClick:function(e, row){ //trigger an alert message when the row is clicked
        //alert("Row " + row.getData().player_slot + " Clicked!!!!");
		var rowHero = document.getElementsByClassName('hero_'+(row.getData().player_slot))
		for (i=0;i<rowHero.length;i++)
		{
			if (rowHero[i].hidden )
			{
				rowHero[i].hidden = false
			}else
			{
				rowHero[i].hidden=true
			}
		//rowHero[i].hidden = true
		}


    },


});

//load sample data into the table
$("#radiant-table").tabulator("setData", radianttabledata);

$("#dire-table").tabulator("setData", diretabledata);

$(window).resize(function(){
    $("#radiant-table").tabulator("redraw");
	 $("#dire-table").tabulator("redraw");
});

$(document).ready(function(){
	for (row=0;row<=10;row++)
	{
		var rowHero  = document.getElementsByClassName('hero_'+row)
		for (i=0;i<rowHero.length;i++)
		{
			rowHero[i].hidden=true
		}

	}
});
