<script lang="ts">
  import Carousel from 'svelte-carousel';
  import avatar from '$lib/images/avatar.jpeg';
</script>

<div class="container mx-auto px-4 py-8">
  <div class="text-center">
    <h1 class="text-3xl font-bold mb-4">LLaMp</h1>
    <p class="h3 mb-8">Dedicated to exploring the boundaries of knowledge.</p>
  </div>

  <section class="mb-12">
    <h2 class="text-2xl font-bold mb-4">Meet Our Team</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div class="text-center">
        <img src={avatar} alt="Member 1" class="mx-auto w-24 h-24 rounded-full mb-2" />
        <p class="font-semibold text-xl">Member 1</p>
        <p class="text-gray-500 text-md">Title 1</p>
      </div>
      <!-- Repeat for other members -->
      <div class="text-center">
        <img src={avatar} alt="Member 2" class="mx-auto w-24 h-24 rounded-full mb-2" />
        <p class="font-semibold text-xl">Member 2</p>
        <p class="text-gray-500 text-md">Title 2</p>
      </div>
      <div class="text-center">
        <img src={avatar} alt="Member 3" class="mx-auto w-24 h-24 rounded-full mb-2" />
        <p class="font-semibold text-xl">Member 3</p>
        <p class="text-gray-500 text-md">Title 3</p>
      </div>
    </div>
  </section>

  <section class="mb-12">
    <h2 class="text-2xl font-bold mb-4">Recent Publications</h2>
    <ul class="space-y-4">
      <li class="border p-4 rounded shadow">
        <h3 class="text-xl font-bold">Title of Paper 1</h3>
        <p>Abstract of Paper 1.</p>
        <a href="#" class="text-blue-500">Read More</a>
      </li>
      <!-- Repeat for other papers -->
    </ul>
  </section>

  <section class="mb-12">
    <h2 class="text-2xl font-bold mb-4">Another Subtopic</h2>
    <p>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa similique vitae doloribus quos
      voluptatibus harum a ad et, distinctio cum molestiae accusamus natus asperiores quasi quidem
      culpa hic totam placeat blanditiis. Facilis, aliquid. Minus nesciunt velit error, officiis a
      ducimus, aperiam, optio doloremque ad voluptatum possimus sed esse ipsa ipsum natus hic
      dignissimos dolore doloribus eaque laboriosam quibusdam sit commodi unde distinctio! Dolores
      sint error dolore, hic explicabo ullam voluptates reprehenderit molestiae harum facilis
      nostrum officiis quaerat unde itaque fuga a saepe labore dolor nulla provident, obcaecati
      rerum recusandae blanditiis sequi! Quisquam, nostrum eos voluptatum modi illo harum inventore
      id.
    </p>
  </section>

  <section class="mb-12">
    <h2 class="text-2xl font-bold mb-4">Affiliated Groups</h2>
    <Carousel autoplay duration={500} arrows={false} swiping={false} particlesToShow={3}>
      <div class="p-2">
        <a href="#" target="_blank" rel="noreferrer">
          <div class="border p-4 rounded shadow">
            <img src="group1.jpg" alt="Materials Project" class="w-full rounded mb-4" />
            <h3 class="text-xl font-bold">Materials Project</h3>
            <p>Description</p>
          </div>
        </a>
      </div>
      <div class="p-2">
        <a href="#" target="_blank" rel="noreferrer">
          <div class="border p-4 rounded shadow">
            <img src="group1.jpg" alt="Group 1" class="w-full rounded mb-4" />
            <h3 class="text-xl font-bold">Group 1</h3>
            <p>Description of Group 1.</p>
          </div>
        </a>
      </div>
      <div class="p-2">
        <a href="#" target="_blank" rel="noreferrer">
          <div class="border p-4 rounded shadow">
            <img src="group1.jpg" alt="Group 1" class="w-full rounded mb-4" />
            <h3 class="text-xl font-bold">Group 1</h3>
            <p>Description of Group 1.</p>
          </div>
        </a>
      </div>
    </Carousel>

    <!-- Repeat for other groups -->
  </section>
  <section class="mb-12 flex flex-wrap md:flex-nowrap">
    <div class="md:w-1/2 p-4">
      <h2 class="text-2xl font-bold mb-4">Citations</h2>
      <pre class="bg-gray-100 p-4 rounded overflow-auto text-black">
		{`
		@article{author2023,
			title={Title of Article},
			author={Author Name},
			journal={Journal Name},
			year={2023}
		`}
      <!-- More citations -->
    </pre>
    </div>
    <div class="md:w-1/2 p-4">
      <h2 class="text-2xl font-bold mb-4">Acknowledgements</h2>
      <p>
        We would like to extend our gratitude to...
        <!-- More acknowledgements -->
      </p>
    </div>
  </section>

  <footer class="text-center mt-8">© 2023 LLaMP. All Rights Reserved.</footer>
</div>
