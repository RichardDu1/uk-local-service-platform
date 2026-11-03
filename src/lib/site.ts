import dataset from '../data/tiling_pseo_dataset.json';

export const SITE_URL = 'https://approvedtilers.co.uk';
export const SITE_NAME = 'Approved Tilers UK';
export const ORG_ID = `${SITE_URL}/#organization`;

export type PageData = (typeof dataset)[number];

/** Absolute, slash-less URL for a site path (matches sitemap & build.format 'file'). */
export function absUrl(path: string): string {
  const clean = path.replace(/\.html$/, '').replace(/\/index$/, '').replace(/\/+$/, '');
  return clean ? `${SITE_URL}${clean.startsWith('/') ? '' : '/'}${clean}` : `${SITE_URL}/`;
}

/** Parse "£1400 - £1550" / "£1280+" into numbers. */
export function parsePrice(range?: string): { low?: number; high?: number } {
  const nums = (range || '').replace(/,/g, '').match(/\d+/g)?.map(Number) || [];
  return { low: nums[0], high: nums[1] };
}

export const services = [...new Map(dataset.map((d) => [d.service_slug, d])).values()].map((d) => ({
  slug: d.service_slug,
  name: d.service_name,
  summary: d.summary,
  duration: d.typical_duration,
  popularTiles: d.popular_tiles,
  checklist: d.checklist,
  process: d.service_process,
}));

export const cities = [...new Map(dataset.map((d) => [d.city_slug, d])).values()]
  .map((d) => ({
    slug: d.city_slug,
    city: d.city,
    county: d.county,
    postcode: d.postcode,
    region: d.region,
  }))
  .sort((a, b) => a.city.localeCompare(b.city));

export const regions = [...new Set(cities.map((c) => c.region))].sort();

export function pagesForService(slug: string): PageData[] {
  return dataset.filter((d) => d.service_slug === slug);
}

export { dataset };
