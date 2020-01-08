// readclassname= function(className){
// 	var x=className;
// 	if(x=="people-purple")
// 	{
// 		return 1;
// 	}
// 	else if(x=="thing-yellow"){
// 		return 2;
// 	}
// 	else if(x=="time-blue"){
// 		return 3;
// 	}
// 	else if(x=="location-green"){
// 		return 4;
// 	}


// }
setrole=function(x,y){

		if(x=="people-purple")
	{
		switch(y){
			case 1:
			   return String("参与方");
			   break;
			case 2:
			   return String("签署方");
			   break;			   
			case 3:
			   return String("设施修建方");
			   break;
			case 4:
			   return String("举办方");
			   break;


		}
		 
		
	}
	else if(x=="location-green"){
		switch(y){
			case 1:
			   return String("地点");
			   break;
			case 2:
			   return String("签署地点");
			   break;			   
			case 3:
			   return String("设施地点");
			   break;
			case 4:
			   return String("活动地点");
			   break;


	}}
	else if(x=="thing-yellow"){
		switch(y){
			// case 1:
			// return String("错误");
			// break;

			case 2:
			   return String("文件");
			   break;			   
			case 3:
			   return String("设施名称");
			   break;
			case 4:
			   return String("活动名称");
			   break;


	}}
	else if(x=="custom-underline"){
		switch(y){
			case 1:
			return String("会见会谈");
			break;

			case 2:
			   return String("签署文件");
			   break;			   
			case 3:
			   return String("设施启用");
			   break;
			case 4:
			   return String("举行活动");
			   break;


	}}
	else {
		switch(y){
			case 1:
			   return String("时间");
			   break;
			case 2:
			   return String("签署时间");
			   break;			   
			case 3:
			   return String("启用时间");
			   break;
			case 4:
			   return String("活动时间");
			   break;


	}}


}