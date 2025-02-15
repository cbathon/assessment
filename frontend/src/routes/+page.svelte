<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    
    type Order = {
      id: number;
      burgers: number;
      fries: number;
      drinks: number
    };
  
    let driveThruMessage = $state('');
    let errorMessage = $state('');
    let orderHistory: Order[] = $state([]);
    let totalBurgers = $derived(orderHistory.reduce((acc, order) => acc + order.burgers, 0));
    let totalFries = $derived(orderHistory.reduce((acc, order) => acc + order.fries, 0));
    let totalDrinks = $derived(orderHistory.reduce((acc, order) => acc + order.drinks, 0));
  
    async function handleSubmit() {
        errorMessage = '';
        const response = await fetch('http://localhost:8000/orders', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: driveThruMessage })
        });

        const data = await response.json();
        if (!response.ok || data.error) {
            errorMessage = data.error;
            return;
        }

        const responseData = await fetch('http://localhost:8000/orders', {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
            }
        });

        const updatedData = await responseData.json();
        orderHistory = updatedData.orderHistory;

        driveThruMessage = '';
    }
        
  </script>
  
  <div class="container mx-auto p-6 max-w-4xl">
    <div class="grid grid-cols-3 gap-6 mb-10">
      <div class="border rounded-lg p-10 text-center">
        <h2 class="text-lg mb-2">Total # of burgers</h2>
        <div class="text-2xl font-bold">{totalBurgers}</div>
      </div>
      
      <div class="border rounded-lg p-10 text-center">
        <h2 class="text-lg mb-2">Total # of fries</h2>
        <div class="text-2xl font-bold">{totalFries}</div>
      </div>
      
      <div class="border rounded-lg p-10 text-center">
        <h2 class="text-lg mb-2">Total # of drinks</h2>
        <div class="text-2xl font-bold">{totalDrinks}</div>
      </div>
    </div>
  
    <div class="mb-10">
      <div class="flex gap-4">
        <input
          type="text"
          bind:value={driveThruMessage}
          placeholder='Ex: "I would like one burger and an order of fries"'
          class="flex-1 p-3 border rounded-lg"
        />
        <Button on:click={handleSubmit} variant="default" size="lg">
          Run
        </Button>
      </div>
      {#if errorMessage}
        <div class="text-red-500">{errorMessage}</div>
      {/if}
    </div>
  
    <div>
      <h2 class="text-xl mb-4">Order History</h2>
      <div class="space-y-3">
        {#each orderHistory as order}
          <div class="border rounded-lg p-4 flex justify-between items-center">
            <div>Order #{order.id}</div>
            <div>
              {#if order.burgers > 0}
                {order.burgers} {order.burgers === 1 ? 'Burger' : 'Burgers'}
              {/if}
              {#if order.fries > 0}
                {order.fries} {order.fries === 1 ? 'Fry' : 'Fries'}
              {/if}
              {#if order.drinks > 0}
                {order.drinks} {order.drinks === 1 ? 'Drink' : 'Drinks'}
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
  
  <style>
    input {
      font-size: 1rem;
    }
  </style>
  
  