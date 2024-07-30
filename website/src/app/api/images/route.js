import fs from "fs";
import path from "path";
import { NextResponse } from "next/server";

export async function GET(request) {
	const imagesDirectory = path.join(process.cwd(), "public/data/images");
	const filenames = fs.readdirSync(imagesDirectory);
	// console.log(filenames);
	const images = filenames.map((name) => path.join("/data/images", name));

	return NextResponse.json(images);
}
