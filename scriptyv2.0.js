function get_irc_log()
{
	var i;
	var element;
	var all_elements;
	var file;
	var xhttp;

	all_elements = document.getElementsByTagName("*");

	for (i = 0; i < all_elements.length; i++) {
		element = all_elements[i];

		file = element.getAttribute("irc-messages");
		if (file) {
			xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				/* Ew javascript is gross */
				if (this.readyState == 4) {
					if (this.status == 200) {
						element.innerHTML = this.responseText;
					} else {
					}
				}
			}
			xhttp.open("GET", file, true);
			xhttp.send();
			return;

		}
	}
}

function update_page()
{
	/* update on every 1000 milliseconds */
	window.setInterval(function() {
		get_irc_log();
	}, 1000);
}

update_page();
