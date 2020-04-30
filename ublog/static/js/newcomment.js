window.onload = function(){
  submit = document.getElementById('submit')
  var fields = new Array('user','email','comment')
  if(submit.addEventListener){
    submit.addEventListener('click',function(e){
          var check = checkformdata(fields, 'error', '');
          if(!check && e.preventDefault) {
            alert('Please fill out all required fields.');
            e.preventDefault();
          } else if(check && e.target.value!='Checked and ready to go!' && e.preventDefault ){
            var obj; //will hold temp pointer
            for(var i=0;i<fields.length;i++){
              field = document.getElementById(fields[i]);
              field.style.display='none';
              obj = document.createElement('div');
              obj.className = 'inputpreview';
              if (field.tagName.toLowerCase() == 'textarea'){
                obj.innerHTML = field.value.replace(/\n/g, '<br />');
                obj.name = field.name;
                obj.id = field.id;
              } else if(field.tagName.toLowerCase() == 'input') {
                obj.appendChild(document.createTextNode(field.value));
                obj.name = field.name;
                obj.id = field.id;
              } else {
                obj.appendChild(document.createTextNode(field.innerHTML));
              }
              field.parentNode.appendChild(obj)
            }
            e.target.value ='Checked and ready to go!';
            e.preventDefault();
          }
        } , false );
  } else if( submit.attachEvent ){
    submit.attachEvent('onclick', function(){ return checkformdata(fields, 'error', '') });
  }
}
