<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;

	let isBullish = false;
</script>

<div class="p-6">
	<!-- <div class="py-6 text-5xl font-semibold">hello world</div> -->

	<!-- add a loading state 	 -->
	{#if !data}
		<div>Loading...</div>
	{:else}
		<div class="flex flex-col gap-5">
			<div class="flex flex-col">
				<div class="flex items-center gap-2">
					<div class="text-5xl uppercase">{data.ticker}</div>
					<div class="text-sm">
						{#if data.ticker_info.open < data.ticker_info.close}
							<span class="bg-success text-success-content rounded-full p-2">Bullish 👍</span>
						{:else}
							<span class="bg-error text-error-content rounded-full p-2">Bearish 👎</span>
						{/if}
					</div>
				</div>

				<div class="text-sm font-thin">
					<div>
						<span class="font-semibold">Location:</span>
						{data.ticker_info.city}, {data.ticker_info.state}
					</div>
					<div><span class="font-semibold">Website:</span> {data.ticker_info.website}</div>
					<div>
						<span class="font-semibold">Employees:</span>
						{data.ticker_info.fullTimeEmployees}
					</div>
					<div><span class="font-semibold">Open:</span> {data.ticker_info.open}</div>
					<div><span class="font-semibold">Low:</span> {data.ticker_info.dayLow}</div>
					<div><span class="font-semibold">Close:</span> {data.ticker_info.dayHigh}</div>
				</div>
			</div>

			<div class="">
				<div class="font-semibold">Predictions</div>
				<div class="flex gap-2 overflow-auto">
					{#each data.predicted_prices as price}
						<div class="bg-primary rounded p-6">
							<div class="w-full">{price.date}</div>
							<div class="w-full">${price.price}</div>
						</div>
					{/each}
				</div>
			</div>

			<div>
				<div class="font-semibold">Description:</div>
				<div>{data.ticker_info.longBusinessSummary}</div>
			</div>
		</div>
		<a class="btn btn-primary" href="http://localhost:5173">click me</a>

		<div class="my-2 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
			{#each data.predicted_prices as price}
				<div class="bg-base-300 rounded p-2">
					<div class="w-full">{price.date}</div>
					<div class="w-full">${price.price}</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
