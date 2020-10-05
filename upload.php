<?php
if (isset($_POST['submit'])) {
	$file = $_FILES['file'];

	$fileName = $_FILES['file']['name'];
	$fileTmpName = $_FILES['file']['tmp_name'];
	$fileSize = $_FILES['file']['size'];
	$fileError = $_FILES['file']['error'];
	$fileType = $_FILES['file']['type'];

	$fileExt = explode('.', $fileName); # take apart the string
	$fileActualExt = strtolower(end($fileExt));

	$allowed = array('webm', 'mpg', 'mp4', 'm4p', 'avi', 'mov', 'wmv', 'mpeg');

	if (in_array($fileActualExt, $allowed)) {
		if ($fileError === 0) {
			# $fileNameNew = uniqid('', true).".".$fileActualExt; # gives a unique name based on milliseconds currently
			$fileDestination = 'uploads/'.$fileName;
			move_uploaded_file($fileTmpName, $fileDestination);
			header("Location: index.php?uploadsuccess");
		} else {
			echo "There was an error uploading your file!";
		}
	} else {
		echo "You cannot upload files of this type!";
	}
}
?>
