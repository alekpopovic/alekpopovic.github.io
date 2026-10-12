require 'json'
require 'cgi'
require 'fileutils'
require 'time'

module SiteFeatures
  def self.absolute(site, path)
    site.config['url'].to_s.sub(%r{/$}, '') + site.config['baseurl'].to_s + path
  end

  def self.text(value)
    html = value.to_s.sub(/\A\s*\{% raw %\}\s*/, '').sub(/\s*\{% endraw %\}\s*\z/, '')
    CGI.unescapeHTML(html.gsub(/<[^>]*>/, ' ')).gsub(/\s+/, ' ').strip
  end

  def self.modified_at(post)
    Time.parse((post.data['last_modified_at'] || post.date).to_s)
  end

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      books = site.data.fetch('books', [])
      person = { '@type' => 'Person', '@id' => SiteFeatures.absolute(site, '/about/#person'),
                 'name' => site.config['author']['name'], 'url' => SiteFeatures.absolute(site, '/about/'),
                 'sameAs' => %w[github linkedin x].map { |key| site.config['author'][key] }.compact }
      documents = site.pages + site.posts.docs
      documents.each do |page|
        next unless page.data['layout']
        book = books.find { |item| item['id'] == page.data['book_id'] }
        image = if page.is_a?(Jekyll::Document)
                  "post-#{page.data['slug']}"
                elsif book
                  "book-#{book['id']}"
                elsif page.data['project_id']
                  "project-#{page.data['project_id']}"
                elsif page.url == '/codepop/'
                  'codepop'
                elsif page.url == '/ai/'
                  'ai'
                else
                  'site'
                end
        page.data['social_image'] = "/assets/social/#{image}.png"
        url = SiteFeatures.absolute(site, page.url)
        schema = { '@type' => 'WebPage', '@id' => url, 'url' => url,
                   'name' => page.data['title'] || site.config['title'],
                   'description' => page.data['description'] || site.config['description'],
                   'inLanguage' => 'en' }
        if page.data['layout'] == 'post'
          schema.merge!('@type' => 'BlogPosting', 'headline' => page.data['title'],
                        'author' => { '@id' => person['@id'] },
                        'image' => SiteFeatures.absolute(site, page.data['social_image']),
                        'datePublished' => page.date.iso8601,
                        'dateModified' => SiteFeatures.modified_at(page).iso8601,
                        'mainEntityOfPage' => url, 'articleSection' => page.data['category'])
        elsif page.data['layout'] == 'book-overview'
          book_author = book['schema_author'] || (book['author'] == person['name'] ? { '@id' => person['@id'] } : { '@type' => 'Organization', 'name' => book['author'] })
          schema['mainEntity'] = { '@type' => 'Book', '@id' => "#{url}#book", 'name' => book['title'],
            'description' => book['description'], 'author' => book_author,
            'inLanguage' => book['language'], 'bookEdition' => book['edition'], 'url' => url,
            'image' => SiteFeatures.absolute(site, page.data['social_image']),
            'isAccessibleForFree' => true,
            'encoding' => %w[pdf epub].map { |format| { '@type' => 'MediaObject',
              'encodingFormat' => format == 'pdf' ? 'application/pdf' : 'application/epub+zip',
              'contentUrl' => SiteFeatures.absolute(site, book[format]) } } }
          schema['mainEntity']['license'] = book['license_url'] if book['license_url']
        elsif page.data['layout'] == 'book'
          schema['mainEntity'] = { '@type' => 'Chapter', 'name' => book['chapters'][page.data['chapter_index']]['title'],
            'url' => url, 'isPartOf' => { '@id' => SiteFeatures.absolute(site, "#{book['url']}#book") },
            'inLanguage' => book['language'] }
        elsif %w[/about/ /cv/].include?(page.url)
          schema.merge!('@type' => 'ProfilePage', 'mainEntity' => { '@id' => person['@id'] })
        elsif page.url == '/codepop/'
          schema['mainEntity'] = { '@type' => 'Organization', '@id' => 'https://www.codepop.tech/#organization',
            'name' => 'CodePop', 'url' => 'https://www.codepop.tech/en/',
            'description' => page.data['description'], 'founder' => { '@id' => person['@id'] } }
        elsif page.url == '/ai/'
          schema.merge!('@type' => 'CollectionPage', 'about' => { '@type' => 'Thing', 'name' => 'Artificial intelligence' })
          schema['mainEntity'] = { '@type' => 'ItemList', 'itemListElement' => site.posts.docs.select { |post| post.data['section'] == 'ai' }.map.with_index { |post, index|
            { '@type' => 'ListItem', 'position' => index + 1, 'name' => post.data['title'], 'url' => SiteFeatures.absolute(site, post.url) } } }
        end
        graph = [person, schema]
        if page.url == '/'
          graph << { '@type' => 'WebSite', '@id' => "#{url}#website", 'url' => url,
                     'name' => site.config['title'], 'publisher' => { '@id' => person['@id'] } }
        end
        page.data['structured_data'] = JSON.generate({ '@context' => 'https://schema.org', '@graph' => graph }).gsub('<', '\\u003c')
      end

      converter = site.find_converter_instance(Jekyll::Converters::Markdown)
      index = site.posts.docs.map do |post|
        { title: post.data['title'], url: post.url, type: 'posts',
          label: post.data['category'], description: post.data['description'],
          text: SiteFeatures.text(converter.convert(post.content)), tags: post.data['tags'] }
      end
      books.each do |book|
        index << { title: "#{book['title']}: #{book['subtitle']}", url: book['url'], type: 'books',
                   label: 'Complete book', description: book['description'], text: book['description'] }
        book['chapters'].each do |chapter|
          source = site.pages.find { |page| page.url == chapter['url'] }
          index << { title: chapter['title'], url: chapter['url'], type: 'chapters', label: book['title'],
                     description: "#{chapter['label']} · #{chapter['reading_minutes']} min read", text: SiteFeatures.text(source&.content) }
        end
      end
      site.data.fetch('video_playlists', []).each do |playlist|
        playlist['videos'].each do |video|
          index << { title: video['title'], url: "/videos/?video=#{video['id']}##{playlist['slug']}", type: 'videos',
            label: playlist['title'], description: "#{video['duration']} · #{playlist['description']}", text: video['title'] }
        end
      end
      site.data.fetch('projects', []).each do |project|
        index << { title: project['name'], url: "/projects/#{project['id']}/", type: 'projects', label: project['category'],
          description: project['description'], text: [project['problem'], project['approach'], project['result'], project['stack'].join(' ')].join(' ') }
      end
      %w[/about/ /contact/ /cv/ /codepop/ /ai/ /learn/ /subscribe/ /updates/ /offline/].each do |path|
        page = site.pages.find { |item| item.url == path }
        next unless page
        text = SiteFeatures.text(page.content)
        if path == '/cv/'
          cv = site.data.fetch('cv', {})
          text = [cv['headline'], cv['summary'], cv['location'],
            cv.fetch('experience', []).flat_map { |job| [job['company'], job['description'], job['context'],
              job.fetch('roles', []).flat_map { |role| [role['title'], role['since'], role['until'] || 'Present', role['location'], role['skills']] }] },
            cv.fetch('skills', []).flat_map { |group| [group['title'], group['description'], group['items']] }].flatten.compact.join(' ')
        end
        index << { title: page.data['title'], url: path, type: 'pages', label: 'Page', description: page.data['description'], text: text }
      end
      site.data.fetch('learning_paths', []).each do |path|
        index << { title: path['title'], url: "/learn/#{path['id']}/", type: 'pages', label: 'Learning path',
          description: path['description'], text: [path['prerequisites'], path['outcome'], path['steps'].map { |step| step.values.join(' ') }].flatten.join(' ') }
      end
      add_page(site, 'search-index.json', JSON.generate(index), 'noindex' => true, 'sitemap' => false)
      urls = documents.select { |page| page.data['layout'] && page.data['sitemap'] != false && !page.data['noindex'] }
      xml = urls.map { |page| "<url><loc>#{CGI.escapeHTML(SiteFeatures.absolute(site, page.url))}</loc></url>" }.join
      add_page(site, 'sitemap.xml', "<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">#{xml}</urlset>")
      entries = site.posts.docs.reverse.first(30).map do |post|
        url = CGI.escapeHTML(SiteFeatures.absolute(site, post.url))
        "<entry><title>#{CGI.escapeHTML(post.data['title'])}</title><id>#{url}</id><link href=\"#{url}\"/><updated>#{SiteFeatures.modified_at(post).iso8601}</updated><summary>#{CGI.escapeHTML(post.data['description'])}</summary><author><name>#{CGI.escapeHTML(site.config['author']['name'])}</name></author></entry>"
      end.join
      root = CGI.escapeHTML(SiteFeatures.absolute(site, '/'))
      updated = site.posts.docs.map { |post| SiteFeatures.modified_at(post) }.max || site.time
      add_page(site, 'feed.xml', "<?xml version=\"1.0\" encoding=\"UTF-8\"?><feed xmlns=\"http://www.w3.org/2005/Atom\"><title>#{CGI.escapeHTML(site.config['title'])} — Field notes</title><id>#{root}feed.xml</id><link href=\"#{root}feed.xml\" rel=\"self\"/><link href=\"#{root}\"/><updated>#{updated.iso8601}</updated>#{entries}</feed>")
      site.data.fetch('redirects', {}).each do |old_path, target|
        page = Jekyll::PageWithoutAFile.new(site, site.source, '', File.basename(old_path))
        page.data = { 'layout' => 'redirect', 'redirect_to' => target, 'permalink' => old_path, 'sitemap' => false, 'noindex' => true }
        site.pages << page
      end
    end

    def add_page(site, name, content, data = {})
      page = Jekyll::PageWithoutAFile.new(site, site.source, '', name)
      page.content = content
      page.data = { 'layout' => nil, 'sitemap' => false, 'render_with_liquid' => false }.merge(data)
      site.pages << page
    end
  end
end

# GitHub Pages cannot issue server-side redirects for static PDF/EPUB files.
# Preserve the actual download bytes at the previously published addresses.
Jekyll::Hooks.register :site, :post_write do |site|
  site.data.fetch('books', []).each do |book|
    %w[pdf epub].each do |format|
      source = File.join(site.dest, book[format].sub(%r{^/}, ''))
      next unless File.file?(source)
      target = File.join(site.dest, 'books', book['id'], 'downloads', File.basename(source))
      FileUtils.mkdir_p(File.dirname(target))
      FileUtils.cp(source, target)
      book.fetch('legacy_download_filenames', []).each do |name|
        FileUtils.cp(source, File.join(File.dirname(target), "#{name}.#{format}"))
      end
    end
  end
end
