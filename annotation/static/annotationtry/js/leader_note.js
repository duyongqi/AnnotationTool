//import styles from './selectcss.css';
console.log("434");
//document.onmouseup=function replaceSelection() {
function mygreen(){
if (window.getSelection) {
    var selecter = window.getSelection();
    var selectStr = selecter.toString();
    if (selectStr.trim != "") {
        var rang = selecter.getRangeAt(0);
        var ele = document.createElement("span");
        var x=selecter.anchorOffset;
        var y=selecter.extentOffset;
        var len=selecter.anchorNode.length;
        ele.className='nite-writer-pen';
        ele.textContent = selectStr;
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
          console.log("3");

        }
        else{
          console.log("xxx");

          for (var i = 2; i >= 0; i--) {
            var next_bro=(rang.startContainer).nextSibling;
          //console.log(pre_bro.textContent);
          //var documentFragment = rang.extractContents();
          var oldChild =(rang.startContainer).removeChild((rang.startContainer).children[i]);
          //console.log(oldChild);
          oldChild=(document.getElementById("ori")).appendChild(oldChild);
          oldChild=(document.getElementById("ori")).insertBefore(oldChild, next_bro);  }
          //console.log(rang.startContainer) ;

          var oldChild=(document.getElementById("ori")).removeChild((rang.startContainer));

        }

         var bt =document.createElement("button");           //createElement生成button对象
         bt.innerHTML = '删除';
         bt.onclick = function () {                          //绑定点击事件
           console.log("su");
           var documentFragment = rang.extractContents();
           //ele.insertAdjacentText('afterbegin',"hu");
         };
         ele.appendChild(bt);
    }}}