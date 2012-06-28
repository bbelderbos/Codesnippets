javascript:(
  function(){
    var tag = null;  
    var urlElement = findElementId('amazonLink'); 
        
    if(urlElement == null) {
      alert('No results for #amazonLink - does the ID element exist on this page?');
      return;      
    }
    
    url = getUrl(urlElement); 
    
    if(tag == null) {
      tag = prompt("Enter your Amazon tag for the URL: ", "Enter Tracking ID here");
    } 
    
    url = url.split("=");
    copyToClipboard(url[0]+'='+tag); 
    
    
    
    function findElementId(idElement) {
      var urlElement = document.getElementById(idElement);
      return urlElement; 
    }
    
    function getUrl(urlElement) {
      var urlHref = urlElement.href; 
      return urlHref;
    }
    
    function copyToClipboard (text) {
      window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);
    }
    
  }
)()