create_json=function(){
        var event=new Array();
        var tri=document.getElementsByClassName("custom-underline");
        var sp=document.querySelectorAll("span");

        
        for (var i = 0; i < tri.length; i++) {
          var arr_argument=new Array();
          var k_flag=0;
          var temp_id=tri[i].getAttribute("event_id"); 
          var temp_tri_role=setrole(tri[i].className,parseInt(temp_id));
          var temp=tri[i].getAttribute("element_number");
          var temp_large={
                 "@START":tri[i].getAttribute("x"),
                 "@END":tri[i].getAttribute("y"),
                 "@ROLE":temp_tri_role,
                 "#text":tri[i].firstChild.nodeValue
             };         
          for ( var j = 0; j < sp.length; j++) {
            if((sp[j].getAttribute("element_number")==temp)&&
              (sp[j].id!=tri[i].id)){
              var temp_role=setrole(sp[j].className,parseInt(temp_id));
              var temp_small={
                 "@START":sp[j].getAttribute("x"),
                 "@END":sp[j].getAttribute("y"),
                 "@ROLE":temp_role,
                 "#text":sp[j].firstChild.nodeValue
             };
            arr_argument[k_flag]=temp_small;  
            k_flag+=1;       
            }
          }                 
          var one_event={
            "@ID":parseInt(temp_id),
            "@TYPE":temp_tri_role,
            event_trigger:temp_large,
            event_argument:arr_argument
          };
          event[i]=one_event;
          

        }
        var ID = document.getElementById("filename").textContent;
        var final_jn={
            "Document": {
                "@ID": ID,
                 event
        }}; 
        return final_jn;
    }


        


      
