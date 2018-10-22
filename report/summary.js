var first_hero = false;
var index = 1
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
        cell.getElement().sparkline(cell.getValue(), {width:"100%", type:"tristate", barWidth:35, disableTooltips:true});
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
	layout:"fitColumns",
	//height:450,
	//responsiveLayout:true,
	//fitColumns:true, //fit columns to width of table (optional)
	//groupBy:"type",
	//groupToggleElement:"header",
	//groupStartOpen:false,
	
    columns:[ //Define Table Columns
			{title:"SN",width:20,field:"player_lobby"},
			
			/*,formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if(value.indexOf("hero_") != -1){
						return "";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return value;
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
				}*/
				//,width:68
			{field:"avatar",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if ("undefined"  != typeof value){
					if (value !=null)
					{
				
					if(value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}}
					}
				}},
			/*{field:"rank_tier",title:"Rank",width:68,formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if ("undefined"  != typeof value){
					if (value !=null)
					{
				
	
						return "<div class=\"rank\"><img src='res\\180px-SeasonalRank"+value + ".png max-width:100%;max-height:100%;/></div>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
					}
				}},*/ //, width:150
			{title:"Player",align:"center",field:"name"},
			{title:"Solo MMR", field:"solo_mmr"},
			{title:"Group MMR", field:"group_mmr"},
			{title:"Est MMR", field:"mmr_estimate"},
			{title:"Match History", field:"matches_win_history", formatter:tristateFormatter}, //,width:200
			{title:"GPM Box Plot", field:"gpm_hisotry", formatter:boxFormatter }, //,width:200
			{title:"Details", field:"account_id", formatter:function(cell, formatterParams){ //,width:200
				   var value = cell.getValue();
					if ("undefined"  != typeof value){
					if (value !=null)
					{
				
					if(JSON.stringify(cell.getData()).indexOf("account_id") >=0){ // account row
						return "<a target=\"_blank\" href='https://zh.dotabuff.com/players/"+value + "'\">details</a>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					//}else{  // hero row
					//	return "<a href='http://dotamax.com/match/details/"+value + "'>details</a>";
					//	//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}}
					}
				}}

    ],
	

	rowFormatter:function(row){
        //row - row component

        var data = row.getData();
		
		if (data.class =="player"){
			row.getElement()[0].classList.add("player_row")
			row.getElement()[0].classList.add("player_row_lobby_"+data.player_lobby)
			first_hero = true;
			index=1;
			
		}else if (data.class =="hero")
		{
			var element = row.getElement(),
			width = element.outerWidth(),
			table;

			//clear current row data
			
			element.empty();
			
			table = $("<table class=\"player_hero\" id='heroes_tbl_for_player_"+data.player_lobby+"' tyle=\"margin-left:auto;margin-right:auto;text-overflow:ellipsis;align-content: center;background-color:text-align:center; black;border: 1px;font-size: 14px;text-align: center;font-family: monospace;color: white;\"><tr></tr></table>");
			$("tr", table).append("<td class='hero_index ' style=\"width: 2%;text-align: center;color:white\">" + index + "</td>");
			
			$("tr", table).append("<td class='hero_img ' style=\"width:8%\"><img src='" + data.hero_img + "'></td>");
			$("tr", table).append("<td class='hero_name ' style=\"width:18%;text-align: left;color:blue\">" + data.hero_name + "</td>");
			
			
			switch(data.skill)
			{
				case 1:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #999999;\"> Normal </td>");
				break;
				case 2:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #E6E8FA;\"> High </td>");
				break
				case 3:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #f0a868;\"> Very High </td>");
				break;
				default:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: red;\"> "+data.skill+" </td>");
				break;
			}
			
		
			if (data.win_lose==1){
				$("tr", table).append("<td class='hero_name ' style=\"width:14%;color: #499249 !important;\"> Win </td>");
			}else if (data.win_lose==-1){
				$("tr", table).append("<td class='hero_name ' style=\"width:14%;color: #c23c2a !important;\"> Lost </td>");
			}
		
			
			
			
			
			
			
			$("tr", table).append("<td class='hero_period ' style=\"width:15%;color:white\">" + data.period + "</td>");
			$("tr", table).append("<td class='hero_gpm ' style=\"width:10%;color:yellow;\"> " + data.gold_per_min + "</td>");
			$("tr", table).append("<td class='hero_xpm ' style=\"width:10%;color:darkblue;\"> " + data.xp_per_min + "</td>");
			$("tr", table).append("<td class='hero_kda ' style=\"width:30%;color:white\"> " + data.kills + "/"+data.deaths+"/"+data.assists+"</td>");
			$("tr", table).append("<td class='hero_details ' style=\"width:30%;color:white\"> <a target=\"_blank\" href='https://zh.dotabuff.com/matches/"+data.match_id + "'>details</a></td>");
			

			//add row data on right hand side
			//$("tr", table).append("<td><div><strong>Data:</strong> " + data + "</div></td>");

			//append newly formatted contents to the row
			element.append(table);
		
			row.getElement()[0].classList.add("hero_row")
			row.getElement()[0].classList.add("hero_row_lobby_"+data.player_lobby)
			
		

			
			
			first_hero= false;
			index=index+1
		}
		
		
		/*
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
		
		
		}*/

	
		
    },
    
	
	
	rowClick:function(e, row){ //trigger an alert message when the row is clicked
        //alert("Row " + row.getData().player_slot + " Clicked!!!!");
		var rowHero = document.getElementsByClassName('hero_row_lobby_'+(row.getData().player_lobby))
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

$("#radiant-table").tabulator("setData", radianttabledata);
$("#dire-table").tabulator({
    //width:216,
	//height:205, // set height of table, this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    layout:"fitDataFill",
	layout:"fitColumns",
	//layout:"fitColumns",
	//height:450,
	//responsiveLayout:true,
	//fitColumns:true, //fit columns to width of table (optional)
	//groupBy:"type",
	//groupToggleElement:"header",
	//groupStartOpen:false,
	
    columns:[ //Define Table Columns
			{title:"SN", width:20,field:"player_lobby"},
			
			/*,formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if(value.indexOf("hero_") != -1){
						return "";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return value;
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}
				}*/
				
			{field:"avatar",formatter:function(cell, formatterParams){
				   var value = cell.getValue();
					if ("undefined"  != typeof value){
						if (value !=null)
					{
					if(value.indexOf("heroes/") >=0){
						return "<img src='"+value + "' style=\"height:33,width=59,background-size: cover;\"/>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					}else{
						return "<img src='"+value + "' style=\"height:32,width:32\"/>";
						//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}}}
				}},
			{title:"Player",align:"center",field:"name"},
			{title:"Solo MMR", field:"solo_mmr"},
			{title:"Group MMR", field:"group_mmr"},
			{title:"Est MMR", field:"mmr_estimate"},
			{title:"Match History", field:"matches_win_history", formatter:tristateFormatter}, //,width:200
			{title:"GPM Box Plot", field:"gpm_hisotry", formatter:boxFormatter }, //,width:200
			{title:"Details", field:"account_id", formatter:function(cell, formatterParams){ //,width:200
				   var value = cell.getValue();
					if ("undefined"  != typeof value){
					if (value !=null)
					{
				
					if(JSON.stringify(cell.getData()).indexOf("account_id") >=0){ // account row
						return "<a target=\"_blank\" href='https://zh.dotabuff.com/players/"+value + "'\">details</a>";
						//return "<img src='"+value + "' style=\"width:auto;height:auto;\"/>";
						//background-size: cover;
					//}else{  // hero row
					//	return "<a href='http://dotamax.com/match/details/"+value + "'>details</a>";
					//	//return "<img src='"+value + "' style=\"height:50;width:auto;\"/>";;
					}}
					}
				}}

    ],
	

	rowFormatter:function(row){
        //row - row component

        var data = row.getData();
		
		if (data.class =="player"){
			row.getElement()[0].classList.add("player_row")
			row.getElement()[0].classList.add("player_row_lobby_"+data.player_lobby)
			first_hero = true;
			index=1;
			
		}else if (data.class =="hero")
		{
			var element = row.getElement(),
			width = element.outerWidth(),
			table;

			//clear current row data
			
			element.empty();
			
			table = $("<table class=\"player_hero\" id='heroes_tbl_for_player_"+data.player_lobby+"' tyle=\"margin-left:auto;margin-right:auto;text-overflow:ellipsis;align-content: center;background-color:text-align:center; black;border: 1px;font-size: 14px;text-align: center;font-family: monospace;color: white;\"><tr></tr></table>");
			$("tr", table).append("<td class='hero_index ' style=\"width: 2%;text-align: center;color:white\">" + index + "</td>");
			
			$("tr", table).append("<td class='hero_img ' style=\"width:8%\"><img src='" + data.hero_img + "'></td>");
			$("tr", table).append("<td class='hero_name ' style=\"width:18%;text-align: left;color:blue\">" + data.hero_name + "</td>");
			
			
			switch(data.skill)
			{
				case 1:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #999999;\"> Normal </td>");
				break;
				case 2:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #E6E8FA;\"> High </td>");
				break
				case 3:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: #f0a868;\"> Very High </td>");
				break;
				default:
				$("tr", table).append("<td class='hero_skill ' style=\"width:14%;color: red;\"> "+data.skill+" </td>");
				break;
			}
			
		
			if (data.win_lose==1){
				$("tr", table).append("<td class='hero_name ' style=\"width:14%;color: #499249 !important;\"> Win </td>");
			}else if (data.win_lose==-1){
				$("tr", table).append("<td class='hero_name ' style=\"width:14%;color: #c23c2a !important;\"> Lost </td>");
			}
		
			
			
			
			
			
			
			$("tr", table).append("<td class='hero_period ' style=\"width:15%;color:white\">" + data.period + "</td>");
			$("tr", table).append("<td class='hero_gpm ' style=\"width:10%;color:yellow;\"> " + data.gold_per_min + "</td>");
			$("tr", table).append("<td class='hero_xpm ' style=\"width:10%;color:darkblue;\"> " + data.xp_per_min + "</td>");
			$("tr", table).append("<td class='hero_kda ' style=\"width:30%;color:white\"> " + data.kills + "/"+data.deaths+"/"+data.assists+"</td>");
			$("tr", table).append("<td class='hero_details ' style=\"width:30%;color:white\"> <a target=\"_blank\" href='https://zh.dotabuff.com/matches/"+data.match_id + "'>details</a></td>");
			

			//add row data on right hand side
			//$("tr", table).append("<td><div><strong>Data:</strong> " + data + "</div></td>");

			//append newly formatted contents to the row
			element.append(table);
		
			row.getElement()[0].classList.add("hero_row")
			row.getElement()[0].classList.add("hero_row_lobby_"+data.player_lobby)
			
		

			
			
			first_hero= false;
			index=index+1
		}
		
		
		/*
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
		
		
		}*/

	
		
    },
    
	
	
	rowClick:function(e, row){ //trigger an alert message when the row is clicked
        //alert("Row " + row.getData().player_slot + " Clicked!!!!");
		var rowHero = document.getElementsByClassName('hero_row_lobby_'+(row.getData().player_lobby))
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

$("#dire-table").tabulator("setData", diretabledata);




$(window).resize(function(){
    $("#radiant-table").tabulator("redraw");
	 $("#dire-table").tabulator("redraw");
});

$(document).ready(function(){
	for (row=1;row<=10;row++)
	{
		var rowHero  = document.getElementsByClassName('hero_row_lobby_'+row)
		for (i=0;i<rowHero.length;i++)
		{
			rowHero[i].hidden=true		
		}

	}
});

	