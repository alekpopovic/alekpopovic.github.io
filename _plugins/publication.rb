require 'json'

Jekyll::Hooks.register :site, :post_write do |site|
  books = site.data.fetch('books', [])
  pages = %w[/ /ai/ /learn/ /learn/ai-workflows/ /learn/reliable-delivery/ /learn/logs-and-security/ /posts/ /projects/ /cv/ /codepop/ /subscribe/ /updates/ /offline/]
  pages += site.data.fetch('projects', []).map { |project| "/projects/#{project['id']}/" }
  pages += books.flat_map { |book| [book['url'], book['chapters'][1]['url']] }
  pages << site.posts.docs.last.url unless site.posts.docs.empty?
  downloads = books.flat_map do |book|
    %w[pdf epub].map { |format| { 'url' => book[format], 'format' => format } }
  end
  if books.first
    book = books.first
    downloads += %w[pdf epub].map { |format| { 'url' => "/books/#{book['id']}/downloads/#{File.basename(book[format])}", 'format' => format } }
  end
  File.write(File.join(site.dest, 'publication-manifest.json'), JSON.generate({
    'origin' => site.config['url'], 'revision' => ENV.fetch('GITHUB_SHA', 'local'),
    'pages' => pages.uniq, 'downloads' => downloads
  }))
end
