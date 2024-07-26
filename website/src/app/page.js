"use client";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Dashboard() {
	const [images, setImages] = useState([]);
	const [result, setResult] = useState(null);
	const [uploadedImage, setUploadedImage] = useState(null);
	const [loading, setLoading] = useState(false);

	useEffect(() => {
		const fetchImages = async () => {
			try {
				const response = await axios.get("/api/images");
				setImages(response.data);
			} catch (error) {
				console.error("Error fetching images:", error);
			}
		};

		fetchImages();
	}, []);

	const handleImageClick = async (imagePath) => {
		const formData = new FormData();
		const imageBlob = await fetch(imagePath).then((r) => r.blob());
		formData.append("image", imageBlob, "image.jpg");

		setLoading(true);
		setUploadedImage(URL.createObjectURL(imageBlob));
		setResult(null);

		try {
			const response = await axios.post(
				"http://localhost:5000/predict",
				formData,
				{
					headers: {
						"Content-Type": "multipart/form-data",
					},
				}
			);

			setResult(response.data);
		} catch (error) {
			console.error("Error posting image:", error);
		} finally {
			setLoading(false);
		}
	};

	const handleFileUpload = async (event) => {
		event.preventDefault(); // Prevent default form submission behavior
		const file = event.target.file.files[0];
		const formData = new FormData();
		formData.append("image", file);

		setLoading(true);
		setUploadedImage(URL.createObjectURL(file));
		setResult(null);

		try {
			const response = await axios.post(
				"http://localhost:5000/predict",
				formData,
				{
					headers: {
						"Content-Type": "multipart/form-data",
					},
				}
			);

			setResult(response.data);
		} catch (error) {
			console.error("Error uploading image:", error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div
			style={{ padding: "20px" }}
			className="flex bg-inherit flex-1 flex-col text-black w-[100vw] h-[100vh] "
		>
			<h1 className="text-center text-xl font-bold mb-4">Dashboard</h1>
			<div className="p-4 m-4 border-2 border-black rounded-md flex-row flex">
				<div className="mb-4 align-middle items-center flex-1 flex flex-col ">
					<div>
						<h2 className="font-bold text-xl text-center mb-4">
							Upload Image:
						</h2>
					</div>
					<form
						onSubmit={handleFileUpload}
						className="justify-between flex flex-col m-4"
					>
						<input type="file" id="file" name="file" />
						<button
							type="submit"
							className="bg-green-300 m-4 rounded-md justify-center flex align-middle items-center self-center  border-2 border-black p-2 w-[50%]"
						>
							Submit Image
						</button>
					</form>
					{uploadedImage && (
						<div className="flex flex-col items-center">
							<h3 className="mt-4">Uploaded Image:</h3>
							<img
								src={uploadedImage}
								alt="Uploaded"
								className="max-w-[20vh] max-h-[20vh] mt-2"
							/>
							{loading && <p>Loading...</p>}
						</div>
					)}
				</div>
				<div className="border-black pl-4 rounded-md border-l-2 flex flex-2 flex-col">
					<div className="flex">
						<h2 className="font-bold text-xl text-center mb-4">
							Select an image:
						</h2>
					</div>
					<div className="flex flex-wrap">
						{images.map((src, index) => (
							<img
								className="m-4 flex max-w-[20vh] max-h-[20vh]"
								key={index}
								src={src}
								alt={`Image ${index + 1}`}
								style={{ width: "100%", cursor: "pointer" }}
								onClick={() => handleImageClick(src)}
							/>
						))}
					</div>
				</div>
			</div>
			{result && (
				<div
					style={{ marginTop: "20px" }}
					className="flex align-middle flex-col self-center "
				>
					<h2 className="font-bold text-xl mb-2 ">Result</h2>

					<p>Predicted Class: {result.predicted_class}</p>
					<pre className="mb-4">
						{JSON.stringify(result.predictions, null, 2)}
					</pre>
				</div>
			)}
		</div>
	);	
}
