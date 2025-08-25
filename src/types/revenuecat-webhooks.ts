/**
 * RevenueCat Webhook Types
 * Based on RevenueCat API v1.0 webhook documentation
 */

// Store types
export type RevenueCatStore = 
  | 'APP_STORE' 
  | 'PLAY_STORE' 
  | 'STRIPE' 
  | 'AMAZON' 
  | 'MAC_APP_STORE' 
  | 'PROMOTIONAL'
  | 'RC_BILLING';

// Environment types
export type RevenueCatEnvironment = 'PRODUCTION' | 'SANDBOX';

// Period types
export type PeriodType = 'NORMAL' | 'TRIAL' | 'INTRO' | 'GRACE';

// Event types
export type RevenueCatEventType = 
  | 'INITIAL_PURCHASE'
  | 'RENEWAL'
  | 'CANCELLATION'
  | 'UNCANCELLATION'
  | 'NON_RENEWING_PURCHASE'
  | 'SUBSCRIPTION_PAUSED'
  | 'EXPIRATION'
  | 'PRODUCT_CHANGE'
  | 'BILLING_ISSUE'
  | 'REFUND'
  | 'REFUND_REVERSED'
  | 'TRANSFER'
  | 'SUBSCRIPTION_EXTENDED'
  | 'TRIAL_STARTED'
  | 'TRIAL_CANCELLED'
  | 'INVOICE_ISSUANCE'
  | 'TEMPORARY_ENTITLEMENT_GRANT'
  | 'VIRTUAL_CURRENCY_TRANSACTION';

// Subscriber attributes
export interface SubscriberAttributes {
  [key: string]: {
    value: string;
    updated_at_ms: number;
  };
}

// Virtual currency adjustment
export interface VirtualCurrencyAdjustment {
  amount: number;
  currency: {
    code: string;
    name: string;
    description: string;
  };
}

// Base event interface with common fields
export interface BaseRevenueCatEvent {
  type: RevenueCatEventType;
  id: string;
  app_id: string;
  app_user_id: string;
  event_timestamp_ms: number;
  aliases?: string[];
  original_app_user_id?: string;
  subscriber_attributes?: SubscriberAttributes;
  store?: RevenueCatStore;
}

// Purchase-related fields
export interface PurchaseEventFields {
  product_id: string;
  period_type: PeriodType;
  purchased_at_ms: number;
  expiration_at_ms?: number;
  environment: RevenueCatEnvironment;
  entitlement_id?: string | null;
  entitlement_ids?: string[];
  presented_offering_id?: string | null;
  transaction_id: string;
  original_transaction_id: string;
  is_family_share: boolean;
  country_code?: string;
  currency?: string;
  price?: number;
  price_in_purchased_currency?: number;
  takehome_percentage?: number | null;
  offer_code?: string | null;
  tax_percentage?: number | null;
  commission_percentage?: number | null;
  renewal_number?: number | null;
  metadata?: any | null;
}

// Specific event types
export interface InitialPurchaseEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'INITIAL_PURCHASE';
}

export interface RenewalEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'RENEWAL';
}

export interface CancellationEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'CANCELLATION';
  cancel_reason?: string;
}

export interface UncancellationEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'UNCANCELLATION';
}

export interface NonRenewingPurchaseEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'NON_RENEWING_PURCHASE';
}

export interface SubscriptionPausedEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'SUBSCRIPTION_PAUSED';
  auto_resume_at_ms?: number;
}

export interface ExpirationEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'EXPIRATION';
  expiration_reason?: string;
}

export interface ProductChangeEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'PRODUCT_CHANGE';
  old_product_id?: string;
}

export interface BillingIssueEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'BILLING_ISSUE';
  grace_period_expiration_at_ms?: number;
}

export interface RefundEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'REFUND';
  refund_reason?: string;
}

export interface RefundReversedEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'REFUND_REVERSED';
}

export interface TransferEvent extends BaseRevenueCatEvent {
  type: 'TRANSFER';
  transferred_from?: string[];
  transferred_to?: string[];
}

export interface SubscriptionExtendedEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'SUBSCRIPTION_EXTENDED';
  new_expiration_at_ms: number;
}

export interface TrialStartedEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'TRIAL_STARTED';
}

export interface TrialCancelledEvent extends BaseRevenueCatEvent, PurchaseEventFields {
  type: 'TRIAL_CANCELLED';
}

export interface InvoiceIssuanceEvent extends BaseRevenueCatEvent {
  type: 'INVOICE_ISSUANCE';
  product_id: string;
  period_type: null;
  purchased_at_ms: number;
  expiration_at_ms: null;
  environment: RevenueCatEnvironment;
  entitlement_id: null;
  entitlement_ids: null;
  presented_offering_id: null;
  transaction_id: null;
  original_transaction_id: null;
  is_family_share: boolean;
  country_code?: string;
  currency?: string;
  price_in_purchased_currency?: number;
  takehome_percentage: null;
  offer_code: null;
  tax_percentage: null;
  commission_percentage: null;
  metadata: null;
  renewal_number: null;
}

export interface TemporaryEntitlementGrantEvent extends BaseRevenueCatEvent {
  type: 'TEMPORARY_ENTITLEMENT_GRANT';
}

export interface VirtualCurrencyTransactionEvent extends BaseRevenueCatEvent {
  type: 'VIRTUAL_CURRENCY_TRANSACTION';
  adjustments: VirtualCurrencyAdjustment[];
  product_display_name?: string;
  product_id: string;
  purchase_environment: RevenueCatEnvironment;
  source: string;
  transaction_id: string;
  virtual_currency_transaction_id: string;
}

// Union type for all events
export type RevenueCatEvent = 
  | InitialPurchaseEvent
  | RenewalEvent
  | CancellationEvent
  | UncancellationEvent
  | NonRenewingPurchaseEvent
  | SubscriptionPausedEvent
  | ExpirationEvent
  | ProductChangeEvent
  | BillingIssueEvent
  | RefundEvent
  | RefundReversedEvent
  | TransferEvent
  | SubscriptionExtendedEvent
  | TrialStartedEvent
  | TrialCancelledEvent
  | InvoiceIssuanceEvent
  | TemporaryEntitlementGrantEvent
  | VirtualCurrencyTransactionEvent;

// Webhook payload structure
export interface RevenueCatWebhookPayload {
  event: RevenueCatEvent;
  api_version: string;
}

// Type guards
export function isInitialPurchase(event: RevenueCatEvent): event is InitialPurchaseEvent {
  return event.type === 'INITIAL_PURCHASE';
}

export function isRenewal(event: RevenueCatEvent): event is RenewalEvent {
  return event.type === 'RENEWAL';
}