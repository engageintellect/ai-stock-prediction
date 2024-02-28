<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;

	let isBullish = false;

	// Helper function to format number as price
	function formatPrice(number: Number) {
		return number.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
	}

	let predicted_prices = data.predicted_prices.map((price: any) => {
		return {
			date: new Date(price.date).toLocaleDateString('en-US'),
			price: formatPrice(price.price)
		};
	});

	let ticker = {
		info: {
			symbol: data.ticker,
			name: data.ticker_info.shortName,
			currentPrice: formatPrice(data.ticker_info.currentPrice),
			website: data.ticker_info.website,
			city: data.ticker_info.city,
			state: data.ticker_info.state,
			employees: data.ticker_info.fullTimeEmployees.toLocaleString('en-US'),
			sector: data.ticker_info.sectorDisp
		},

		performance: {
			currentPrice: formatPrice(data.ticker_info.currentPrice),
			marketCap: formatPrice(data.ticker_info.marketCap),
			volume: data.ticker_info.volume,
			open: formatPrice(data.ticker_info.open),
			low: formatPrice(data.ticker_info.dayLow),
			close: formatPrice(data.ticker_info.dayHigh)
		},

		analysis: {
			recommendation: data.ticker_info.recommendationKey,
			shortRatio: data.ticker_info.shortRatio,
			shortFloat: `${(data.ticker_info.shortPercentOfFloat * 100).toFixed(2)}%`,
			beta: data.ticker_info.beta,
			fiftyTwoWeekLow: data.ticker_info.fiftyTwoWeekLow,
			fiftyTwoWeekHigh: data.ticker_info.fiftyTwoWeekHigh
		}
	};
</script>

<div class="">
	{#if !data}
		<div>Loading...</div>
	{:else}
		<!-- {JSON.stringify(ticker)} -->
		<!-- {JSON.stringify(predicted_prices)} -->

		<div class="flex flex-col gap-5">
			<div class="flex flex-col">
				<div class="flex items-start gap-2">
					<div class="flex items-center gap-5 text-7xl uppercase">
						<div>
							{ticker.info.symbol}
						</div>
						<div class="badge badge-primary h-full px-4 py-2 text-3xl font-thin">
							{ticker.info.currentPrice}
						</div>
					</div>
					<!-- <div class="text-sm"> -->
					<!-- {#if data.ticker_info.previousClose < data.ticker_info.dayHigh} -->
					<!-- <div class="badge badge-success text-success-content">Bullish 👍</div> -->
					<!-- {:else} -->
					<!-- <div class="badge badge-error text-success-content">Bearish 👎</div> -->
					<!-- {/if} -->
					<!-- </div> -->
				</div>

				<div class="text-xl font-thin uppercase">{ticker.info.name}</div>

				<div class="flex flex-col gap-5 text-sm font-thin">
					<div class="">
						<div>
							<span class="font-semibold">Website:</span>
							<a href={ticker.info.website} target="_blank">{ticker.info.website}</a>
						</div>

						<div>
							<span class="font-semibold">Location:</span>
							{ticker.info.city}, {ticker.info.state}
						</div>

						<div>
							<span class="font-semibold">Employees:</span>
							{ticker.info.employees}
						</div>

						<div>
							<span class="font-semibold">Sector:</span>
							{ticker.info.sector}
						</div>
					</div>
				</div>
			</div>

			<div class="">
				<div class="font-semibold">Analyst Data:</div>
				<div class="flex gap-2 overflow-auto">
					{#each Object.entries(ticker) as [key, value]}
						{#if key !== 'performance'}
							<div class="bg-accent text-accent-content rounded p-6">
								{#each Object.entries(value) as x}
									<div class="flex gap-2">
										<div class="capitalize">{x[0]}:</div>
										<div class="font-thin">{x[1]}</div>
									</div>
								{/each}
							</div>
						{/if}
					{/each}
				</div>
			</div>

			<div class="">
				<div class="font-semibold">Performance Data:</div>
				<div class="flex gap-2 overflow-auto">
					{#each Object.entries(ticker.analysis) as [key, value]}
						<div class="bg-secondary text-secondary-content rounded p-6">
							{#if value}
								<div class="flex flex-col items-center justify-center gap-2">
									<div class="font-thin capitalize">{key}:</div>
									<div class="text-xl font-bold uppercase">{value}</div>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</div>

			<div class="">
				<div class="font-semibold">30 Day Forecast:</div>
				<div class="flex gap-2 overflow-auto">
					{#each data.predicted_prices as price}
						<div class="bg-primary text-primary-content rounded p-6 text-center">
							<div class="w-full text-nowrap text-sm font-thin">{price.date}</div>
							<div class="w-full text-2xl">{formatPrice(price.price)}</div>
						</div>
					{/each}
				</div>
			</div>

			<div>
				<div class="font-semibold">Description:</div>
				<div>{data.ticker_info.longBusinessSummary}</div>
			</div>
		</div>
		<a class="btn btn-primary my-5" href="http://localhost:5173">click me</a>

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
