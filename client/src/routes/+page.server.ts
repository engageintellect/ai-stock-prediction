import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const res = await fetch('http://localhost:6969/api/stock/pltr');
	const data = await res.json();
	return data;
};
