import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
	const res = await fetch(`http://localhost:6969/api/stock/${params.slug}`);
	const data = await res.json();
	return data;
};
