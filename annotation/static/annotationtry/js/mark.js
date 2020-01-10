
      //import styles from './selectcss.css';
          console.log("434");
          //!!!!!!!!!!!!!!!!!!全局变量
 //document.onmouseup=function replaceSelection() {

         
          

flag=0;
 mytrigger=function(class_Name,flag_te,eve_id){
var flag_te=flag;
  flag+=1;

    if (window.getSelection) {
        var selecter = window.getSelection();
        var selectStr = selecter.toString();
        if (selectStr.trim != "") {
            var rang = selecter.getRangeAt(0);
            var ele = document.createElement("span");
            // var x=selecter.anchorOffset;
            var x=selecter.anchorOffset;
            var y=selecter.extentOffset;
            if(x > y){
                x = x;
                y = y + 1;
                var h = x;
                x = y;
                y = h;
            }
            else{
                x = x + 1;
                y = y;
            }
            var len=y-x+1;
            ele.className=class_Name;
            ele.textContent = selectStr;
            // var temp_id=(x.toString())+"_"+(y.toString());
            ele.setAttribute('element_number',flag);
            ele.setAttribute('event_id',eve_id) ;             
            rang.surroundContents(ele);


            

            //before both chorme&page
            var tempo=(rang.startContainer).firstChild;
            var ele_pre=document.createElement("span");
            ele_pre=rang.startContainer.appendChild(ele_pre);
            ele_pre=rang.startContainer.insertBefore(ele_pre, tempo);
            ele_pre.textContent = tempo.textContent;
            (rang.startContainer).removeChild(tempo);


            

        
            //after both chorme&page
            var temp=(rang.startContainer).lastChild;
            var ele_aft=document.createElement("span");
            ele_aft=rang.startContainer.appendChild(ele_aft);
            ele_aft=rang.startContainer.insertBefore(ele_aft, temp);
            //console.log(temp.textContent);
            ele_aft.textContent = temp.textContent;
            (rang.startContainer).removeChild(temp);

            if(rang.startContainer==document.getElementById("ori")){
              ele.setAttribute('x',x);
              ele.setAttribute('y',y);
              var temp_id=(x.toString())+"_"+(y.toString());
              ele.setAttribute('id',temp_id);

            }
            else{
              console.log("xxx");

              if(((rang.startContainer).previousSibling)!=null){
                console.log("yes");
              var z=(rang.startContainer).previousSibling.id;
              var last_len=z.length;
              var i=z.indexOf("_");
              var last_start=Number(z.substr(0,i));
              var last_end=Number(z.substr(i+1,last_len-i));
              x=last_end+x;
              y=x+len-1;
   

              

              }
              var temp_id=(x.toString())+"_"+(y.toString());
              ele.setAttribute('id',temp_id); 
              ele.setAttribute('x',x);
              ele.setAttribute('y',y);              

              



              for (var i = 2; i >= 0; i--) {
                var next_bro=(rang.startContainer).nextSibling;
              //console.log(pre_bro.textContent);
              //var documentFragment = rang.extractContents();
              var oldChild =(rang.startContainer).removeChild((rang.startContainer).children[i]);
              //console.log(oldChild);
              oldChild=(document.getElementById("ori")).appendChild(oldChild);
              oldChild=(document.getElementById("ori")).insertBefore(oldChild, next_bro);  }

              var oldChild=(document.getElementById("ori")).removeChild((rang.startContainer));
                       



            }


            


             var bt =document.createElement("button");           //createElement生成button对象
             bt.innerHTML = '(X)'; 
             bt.setAttribute('type','button');
             ele.appendChild(bt); 
             bt.onclick = function () {                          //绑定点击事件
               // console.log("su");
               var temp1=ele.previousSibling;
               var temp2=ele.nextSibling;
               var pre_text=temp1.textContent;
               var next_text=temp2.textContent;
               var all_text=pre_text+ele.firstChild.nodeValue+next_text;
               
               temp1.textContent=all_text;
               document.getElementById("ori").removeChild(ele);
               document.getElementById("ori").removeChild(temp2);   

               // if(ele.previousElementSibling!=null){console.log("yes");}            



               

             };  
             


           
                
                
            

        }}
        
        

        return flag;


      }
mymark=function (class_Name,flag_te,eve_id)
{
var flag_te=flag;
  if (window.getSelection) {
        var selecter = window.getSelection();
        var selectStr = selecter.toString();
        if (selectStr.trim != "") {
            var rang = selecter.getRangeAt(0);
            var ele = document.createElement("span");
            // var x=selecter.anchorOffset;
            var x=selecter.anchorOffset;
            var y=selecter.extentOffset;
            if(x > y){
                x = x;
                y = y + 1;
                var h = x;
                x = y;
                y = h;
            }
            else{
                x = x + 1;
                y = y;
            }
            var len=y-x+1;
            ele.className=class_Name;
            ele.textContent = selectStr;
            // var temp_id=(x.toString())+"_"+(y.toString());
            ele.setAttribute('element_number',flag);
            ele.setAttribute('event_id',eve_id) ;           
            rang.surroundContents(ele);


            

            //before both chorme&page
            var tempo=(rang.startContainer).firstChild;
            var ele_pre=document.createElement("span");
            ele_pre=rang.startContainer.appendChild(ele_pre);
            ele_pre=rang.startContainer.insertBefore(ele_pre, tempo);
            ele_pre.textContent = tempo.textContent;
            (rang.startContainer).removeChild(tempo);


            

        
            //after both chorme&page
            var temp=(rang.startContainer).lastChild;
            var ele_aft=document.createElement("span");
            ele_aft=rang.startContainer.appendChild(ele_aft);
            ele_aft=rang.startContainer.insertBefore(ele_aft, temp);
            //console.log(temp.textContent);
            ele_aft.textContent = temp.textContent;
            (rang.startContainer).removeChild(temp);

            if(rang.startContainer==document.getElementById("ori")){
              ele.setAttribute('x',x);
              ele.setAttribute('y',y);
              var temp_id=(x.toString())+"_"+(y.toString());
              ele.setAttribute('id',temp_id);

            }
            else{
            

              if(((rang.startContainer).previousSibling)!=null){
                
              var z=(rang.startContainer).previousSibling.id;
              var last_len=z.length;
              var i=z.indexOf("_");
              var last_start=Number(z.substr(0,i));
              var last_end=Number(z.substr(i+1,last_len-i));
              x=last_end+x;
              y=x+len-1;
   

              

              }
              
              var temp_id=(x.toString())+"_"+(y.toString());
              ele.setAttribute('id',temp_id); 
              ele.setAttribute('x',x);
              ele.setAttribute('y',y);
              



              for (var i = 2; i >= 0; i--) {
                var next_bro=(rang.startContainer).nextSibling;
              //console.log(pre_bro.textContent);
              //var documentFragment = rang.extractContents();
              var oldChild =(rang.startContainer).removeChild((rang.startContainer).children[i]);
              //console.log(oldChild);
              oldChild=(document.getElementById("ori")).appendChild(oldChild);
              oldChild=(document.getElementById("ori")).insertBefore(oldChild, next_bro);  }

              var oldChild=(document.getElementById("ori")).removeChild((rang.startContainer));
                       



            }


            


             var bt =document.createElement("button");           //createElement生成button对象
             bt.innerHTML = '(X)'; 
             bt.setAttribute('type','button');
             ele.appendChild(bt); 
             bt.onclick = function () {                          //绑定点击事件
               // console.log("su");
               var temp1=ele.previousSibling;
               var temp2=ele.nextSibling;
               var pre_text=temp1.textContent;
               var next_text=temp2.textContent;
               var all_text=pre_text+ele.firstChild.nodeValue+next_text;
               temp1.textContent=all_text;
               document.getElementById("ori").removeChild(ele);
               document.getElementById("ori").removeChild(temp2);   

               // if(ele.previousElementSibling!=null){console.log("yes");}            



               

             };  
             


           
                
                
            

        }}
        
}



