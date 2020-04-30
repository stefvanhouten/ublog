function checkformdata(fields, errorclass, normalclass){
	var error = false;
	// check normal fields
	for(var i = 0; i < fields.length; i++){
		if(document.getElementById(fields[i])){
		  var obj = document.getElementById(fields[i]);
      if(obj.value.replace(/(^\s+|\s+$)/g, "") == ''){
			  error = true;
			  obj.className = errorclass;
		  } else {
			  obj.className = normalclass;
		  }
		}
	}
  return !error;
}
