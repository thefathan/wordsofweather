/**
 * JavaScript code
 * @version 2022-07-07
 * @since 2022-05-07
 * <ul>
 *   <li>2022-05-07: applied for DB and bootstrap</li>
 *   <li>2022-05-07: rewrite to native (non jQuery) version</li>
 * </ul>
 */
 
const path = "v1/comment";

/**
 * This function will be done just after loading contents.
 */
document.addEventListener("DOMContentLoaded", function(){
	/**
	 * Get current data from server
	 */
	getData();
	/**
	 * Add function to the "Send" button.
	 */
	document.getElementById("send").addEventListener("click", function(){
		postAndGetData();
	});
	/**
	 * Add function to the "Delete All" button.
	 */
	document.getElementById("deleteAll").addEventListener("click", function(){
		if(confirm("Are you sure?")) {
			document.getElementById("city").value = "";
			document.getElementById("content").value = "";
			deleteAndGetData();
		}
	});
});

/**
 * Get all data and update history block.
 */
function getData() {
	fetch(path, {
  	method: "GET"
	}).then(response => response.json())
		.then(data => {
			console.log("[GET] data=" + JSON.stringify(data));
			let hist = document.getElementById("hist");
			hist.innerHTML = ""; 
			for(let i = 0; i < data.length; i++) {
				// let date = new Date(data[i].date);
				let a = "<tr>\n";
				a += "<td>"+data[i].datetime+"</td>\n";
				a += "<td>"+data[i].content+"</td>\n";
				a += "<td>"+data[i].weather+"</td>\n";
				a += "</tr>\n";
				hist.insertAdjacentHTML("beforeend", a);
			}
  });
}

/**
 * Send a data, and then, get data.
 */
function postAndGetData() {
	const param = {
		method: "POST",
  	headers: {'Content-Type': 'application/json;charset=utf-8'},
  	body: JSON.stringify({city: document.getElementById("city").value, 
			 												content: document.getElementById("content").value})
	};
	fetch(path, param)
		.then(response => response.status)
		.then(data => {
			console.log("[POST] body=" + param.body + ", status=" + data);
			getData();
  	});
}

/**
 * Delete all data, and then, get data.
 */
function deleteAndGetData() {
	const param = {
		method: "DELETE",
  	headers: {'Content-Type': 'application/json;charset=utf-8'},
	};
	fetch(path, param)
		.then(response => response.status)
		.then(data => {
			console.log("[DELETE] status=" + data);
			getData();
  	});
}