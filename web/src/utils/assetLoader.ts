/**
 * Asset Loader Utilities
 * Helpers for loading asset metadata and managing asset loading
 */

import type { AssetMetadata } from '../threeScene';

/**
 * Load asset metadata from JSON file
 */
export async function loadAssetMetadata(assetId: string): Promise<AssetMetadata> {
  const response = await fetch(`/assets/meta/${assetId}.json`);

  if (!response.ok) {
    throw new Error(`Failed to load metadata for ${assetId}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Load all asset metadata from asset-list.json
 */
export async function loadAllAssetMetadata(): Promise<AssetMetadata[]> {
  const response = await fetch('/assets/meta/asset-list.json');

  if (!response.ok) {
    throw new Error(`Failed to load asset list: ${response.statusText}`);
  }

  const assetList = await response.json();
  const assetIds = assetList.assets
    .filter((asset: any) => asset.status === 'complete')
    .map((asset: any) => asset.id);

  // Load metadata for each asset
  const metadataPromises = assetIds.map((id: string) => loadAssetMetadata(id));

  return Promise.all(metadataPromises);
}

/**
 * Load assets for a specific section
 */
export async function loadSectionAssets(sectionId: string): Promise<AssetMetadata[]> {
  const allMetadata = await loadAllAssetMetadata();
  return allMetadata.filter((meta) => meta.section === sectionId);
}

/**
 * Preload critical assets (home section)
 */
export async function preloadCriticalAssets(): Promise<AssetMetadata[]> {
  return loadSectionAssets('home');
}

/**
 * Calculate total loading progress
 */
export function calculateProgress(
  loadedAssets: Map<string, number>,
  totalAssets: number
): number {
  if (totalAssets === 0) return 100;

  let totalProgress = 0;
  loadedAssets.forEach((progress) => {
    totalProgress += progress;
  });

  return (totalProgress / totalAssets) || 0;
}

export default {
  loadAssetMetadata,
  loadAllAssetMetadata,
  loadSectionAssets,
  preloadCriticalAssets,
  calculateProgress,
};
