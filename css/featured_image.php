<?php
$bgcolor = "#eff1e1";
$dimensions = array(
  "width" => "200px",
  "height" => "200px",
);
$positions = array(
  1 => "top left",
  2 => "top right",
  3 => "bottom left",
  4 => "bottom right",
);
$border = "#ccc";
$radius = "8px";
$title = array( 
  "color" => "#853328", 
  "size" => "10pt", 
  "position" => array(
    "top" => "90px", 
    "left" => "20px",
  ), 
  "text" => "new blog post",
  "font" => "'Limelight', cursive",
);
$images = array(
  "bg1" => array(
    "url" => "https://twimg0-a.akamaihd.net/profile_images/2357974774/vsuua7vxeim2khmxgjrx_bigger.png",
    "position" => "top left",
  ),
  "bg2" => array(
    "url" => "..",
    "position" => "right bottom",
  ),
  "overlay" => array(
    "url" => "http://peppoj.net/wp-content/uploads/2010/07/512-Terminal.png",
    "position" => "top left",
  ),
);

# form (start simple)
if(isset($_GET['bgcolor'])){
  $bgcolor = $_GET['bgcolor'];
  $title["text"] = $_GET['title'];
  $title["font"] = $_GET['font'];
  $images["bg1"]["url"] = $_GET["bg1_url"];
  $images["bg1"]["position"] = $_GET["bg1_pos"];
  $images["bg2"]["url"] = $_GET["bg2_url"];
  $images["bg2"]["position"] = $_GET["bg2_pos"];
  $images["overlay"]["url"] = $_GET["overlay_url"];
  $images["overlay"]["position"] = $_GET["overlay_pos"];
}
?>
<!DOCTYPE html>
<html>
<head>
<title>Featured image creator for blog post</title>
<link href='http://fonts.googleapis.com/css?family=Limelight' rel='stylesheet' type='text/css'>
<style>
<?php
$css = <<<EOD
body {
  width: 800px;
  font-size: 85%;
}
#wrapper {
  float: right;
  border: 1px solid $border;
  overflow: hidden;
  margin: 88px 0 0 30px;
  width: 222px;
  height: 222px;
  background-color: $bgcolor;
}
#featImg { 
  width: {$dimensions["width"]}; height: {$dimensions["height"]};
  margin: 10px;
  position: relative;

  border: 1px solid $border;
  background-image: url({$images["bg1"]["url"]}), url({$images["bg2"]["url"]});
  background-position: {$images["bg1"]["position"]}, {$images["bg2"]["position"]};
  background-repeat: no-repeat;
}
#featImg, img, #overlay {
  border-radius: $radius; -webkit-border-radius: $radius; -moz-border-radius: $radius;
}
#overlay {
  width: {$dimensions["width"]}; height: {$dimensions["height"]};
  opacity: 0.2;
  background: url({$images["overlay"]["url"]}) {$images["overlay"]["position"]} no-repeat; 
}
h1 {
  color: {$title["color"]};
  font-family: {$title["font"]};
  padding: 2px 5px;
  background-color: rgba(255, 255, 255, .5); 
  z-index: 990;
}
h1#blogtitle {
  width: 160px;
  font-size: {$title["size"]};
  position: absolute;
  top: {$title["position"]["top"]}; left: {$title["position"]["left"]};
}
#formWrapper {
  float: left; 
}
form {
  padding: 10px 5px;
  width: 480px;
}
label {
  clear: both;
  float: left;
  margin: 5px;
  width: 150px;
  padding-top: 5px;
}
input, select {
  border: 1px solid #ddd;
  margin: 5px;
  width: 300px;
  height: 25px;
  float: right;
}
#submit {
  clear: both;
  float: right; 
  width: 150px;
}
EOD;
print $css;
?>
</style>
</head>

<body>
  <div id="wrapper">
    <div id="featImg">
      <h1 id="blogtitle"><?php echo $title["text"]; ?></h1>
      <div id='overlay'></div>
    </div>
  </div>

  <div id="formWrapper">
    <h1>Create Featured Image</h1>
    <form id="addImage" name="addImage" method="get">
      <label>Background Color</label>
      <input name="bgcolor" value="<?php echo $bgcolor; ?>">
      <label>Blog Title</label>
      <input name="title" value="">
      <br>
      <label>Background image #1</label>
      <input name="bg1_url" value="<?php echo $_GET["bg1_pos"]; ?>">
      <label>Position</label>
      <select name="bg1_pos">
      <?php
      foreach($positions as $k=>$v){
        echo "<option value='$k' ";
        if($k == $_GET["bg1_pos"]) echo " selected='selected'";
        echo ">$v</option>";
      }
      ?>
      </select>
      <br>
      <label>Background image #2</label>
      <input name="bg2_url" value="<?php echo $_GET["bg2_url"]; ?>">
      <label>Position</label>
      <select name="bg2_pos">
      <?php
      foreach($positions as $k=>$v){
        echo "<option value='$k' ";
        if($k == $_GET["bg2_pos"]) echo " selected='selected'";
        echo ">$v</option>";
      }
      ?>
      </select>
      <br>
      <label>Overlay image</label>
      <input name="overlay_url" value="<?php echo $_GET["overlay_url"]; ?>">
      <label>Position</label>
      <select name="bg1_pos">
      <?php
      foreach($positions as $k=>$v){
        echo "<option value='$k' ";
        if($k == $_GET["overlay_pos"]) echo " selected='selected'";
        echo ">$v</option>";
      }
      ?>
      </select>
      <input id="submit" value='Create image' type='submit'>
    </form>
  </div>
</body>

</html>
