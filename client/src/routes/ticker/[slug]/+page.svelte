<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;

	let isBullish = false;
</script>

<div class="">
	{#if !data}
		<div>Loading...</div>
	{:else}
		<div class="flex flex-col gap-5">
			<div class="flex flex-col">
				<div class="flex items-start gap-2">
					<div class="text-5xl uppercase">
						{data.ticker} <span class="font-thin">${data.ticker_info.currentPrice}</span>
					</div>
					<div class="text-sm">
						{#if data.ticker_info.previousClose < data.ticker_info.dayHigh}
							<div class="badge badge-success text-success-content">Bullish 👍</div>
						{:else}
							<div class="badge badge-error text-success-content">Bearish 👎</div>
						{/if}
					</div>
				</div>

				<div class="text-xl font-thin uppercase">{data.ticker_info.shortName}</div>

				<div class="flex flex-col gap-5 text-sm font-thin">
					<div class="">
						<div>
							<span class="font-semibold">Website:</span>
							<a href={data.ticker_info.website} target="_blank">{data.ticker_info.website}</a>
						</div>

						<div>
							<span class="font-semibold">Location:</span>
							{data.ticker_info.city}, {data.ticker_info.state}
						</div>

						<div>
							<span class="font-semibold">Employees:</span>
							{data.ticker_info.fullTimeEmployees}
						</div>

						<div>
							<span class="font-semibold">Sector:</span>
							{data.ticker_info.sectorDisp}
						</div>
					</div>

					<!-- <div class="flex flex-col gap-2 sm:flex-row"> -->
					<div class="flex gap-2 overflow-auto">
						<div class="bg-accent text-accent-content w-full rounded p-6">
							<div>
								<span class="font-semibold">Market Cap:</span> ${data.ticker_info.marketCap}
							</div>
							<div><span class="font-semibold">Volume:</span> ${data.ticker_info.volume}</div>
							<div><span class="font-semibold">Open:</span> ${data.ticker_info.open}</div>
							<div><span class="font-semibold">Low:</span> ${data.ticker_info.dayLow}</div>
							<div><span class="font-semibold">Close:</span> ${data.ticker_info.dayHigh}</div>
						</div>

						<div class="bg-accent text-accent-content w-full rounded p-6">
							<div>
								<span class="font-semibold">Recommendation</span>
								{data.ticker_info.recommendationKey}
							</div>
							<div>
								<span class="font-semibold">Short Ratio</span>
								{data.ticker_info.shortRatio}
							</div>
							<div>
								<span class="font-semibold">Short Float</span>
								{data.ticker_info.shortPercentOfFloat * 100}%
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="">
				<div class="font-semibold">Predictions:</div>
				<div class="flex gap-2 overflow-auto">
					{#each data.predicted_prices as price}
						<div class="bg-primary text-primary-content rounded p-6">
							<div class="w-full text-sm font-semibold">{price.date}</div>
							<div class="w-full text-2xl">${price.price}</div>
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
