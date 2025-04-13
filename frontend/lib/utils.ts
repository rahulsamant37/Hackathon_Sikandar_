/**
 * Simple utility function to combine class names
 * This is a simplified version that doesn't require external dependencies
 */
export function cn(...inputs: (string | undefined | null | false)[]) {
  return inputs.filter(Boolean).join(' ');
}
