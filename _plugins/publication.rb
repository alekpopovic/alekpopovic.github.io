require 'json'

Jekyll::Hooks.register :site, :post_write do |site|
  books = site.data.fetch('books', [])
  pages = %w[/ /ai/ /ai/workshops/ /learn/ /learn/workspace/ /learn/start/ /videos/ /posts/ /projects/ /cv/ /codepop/ /codepop/engineering-notes/ /subscribe/ /newsletter/ /updates/ /offline/ /reading/]
  pages += site.data.fetch('learning_paths', []).map { |path| "/learn/#{path['id']}/" }
  pages += site.data.fetch('video_lessons', []).map { |lesson| "/videos/#{lesson['slug']}/" }
  pages += site.data.fetch('newsletters', []).map { |issue| issue['url'] }
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
