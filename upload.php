<?php
if (isset($_POST['submit'])) {
	$file = $_FILES['file'];

	$fileName = $file['name'];
	$fileTmpName = $file['tmp_name'];
	$fileSize = $file['size'];
	$fileError = $file['error'];
	$fileType = $file['type'];
	$fileChosenName = $_POST['title'];

	$fileExt = explode('.', $fileName); # take apart the string
	$fileActualExt = strtolower(end($fileExt));
	$allowed = array('webm', 'mpg', 'mp4', 'm4p', 'avi', 'mov', 'wmv', 'mpeg');

	if (in_array($fileActualExt, $allowed)) {
		if ($fileError === 0) {
			$fileNameNew = $fileChosenName.".".$fileActualExt;
			$fileDestination = 'uploads/'.$fileNameNew;
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
