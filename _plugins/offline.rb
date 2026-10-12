require 'json'
require 'uri'

# A local manifest, rebuilt from the catalog. No external assets are fetched.
Jekyll::Hooks.register :site, :post_write do |site|
  assets = %w[css js fonts icons].flat_map do |directory|
    Dir.glob(File.join(site.dest, 'assets', directory, '**', '*')).select { |path| File.file?(path) }
  end.map { |path| '/' + path.delete_prefix(site.dest + '/') }
  assets.reject! { |path| path.match?(%r{/js/(analytics|ga4-events|effects|ai|posts|videos|cv|search|article|learning|project)\.js$}) || path.end_with?('/ai.css') }
  assets.reject! { |path| path.match?(%r{/js/(labs|learning)/}) || path.end_with?('/library/ai-select.js', '/web-vitals.js', '/ai-shell.css', '/ai-cards.css') }
  assets.reject! { |path| path.include?('/fonts/') && !path.end_with?('.woff2') }
  chapters = site.data.fetch('books', []).flat_map do |book|
    book['chapters'].map do |chapter|
      html = File.read(File.join(site.dest, chapter['url'].sub(%r{^/}, '')))
      images = html.scan(/<img\b[^>]*\bsrc=["']([^"']+)["']/i).flatten.filter_map do |source|
        url = URI.join(site.config['url'] + chapter['url'], source)
        url.path if url.host == URI(site.config['url']).host && url.path.start_with?('/assets/')
      end
      { 'url' => chapter['url'], 'title' => chapter['title'], 'book' => book['title'], 'assets' => images.uniq }
    end
  end
  File.write(File.join(site.dest, 'offline-manifest.json'), JSON.generate({ 'assets' => assets, 'chapters' => chapters }))
end
