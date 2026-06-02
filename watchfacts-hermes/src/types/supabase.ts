export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.5"
  }
  public: {
    Tables: {
      blockchain_passports: {
        Row: {
          certification_reports: Json | null
          contract_address: string | null
          created_at: string | null
          id: string
          listing_id: string | null
          metadata_uri: string | null
          ownership_history: Json | null
          service_records: Json | null
          watch_identity_hash: string | null
        }
        Insert: {
          certification_reports?: Json | null
          contract_address?: string | null
          created_at?: string | null
          id: string
          listing_id?: string | null
          metadata_uri?: string | null
          ownership_history?: Json | null
          service_records?: Json | null
          watch_identity_hash?: string | null
        }
        Update: {
          certification_reports?: Json | null
          contract_address?: string | null
          created_at?: string | null
          id?: string
          listing_id?: string | null
          metadata_uri?: string | null
          ownership_history?: Json | null
          service_records?: Json | null
          watch_identity_hash?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "blockchain_passports_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
        ]
      }
      certification_reports: {
        Row: {
          bezel_condition: Json | null
          blockchain_mint_tx: string | null
          bracelet_condition: Json | null
          case_condition: Json | null
          caseback_engraving: Json | null
          created_at: string | null
          crown_operation: Json | null
          dial_authenticity: Json | null
          dial_condition: Json | null
          hands_authenticity: Json | null
          id: string
          inspector_id: string | null
          inspector_signature_hash: string | null
          listing_id: string | null
          lume_response: Json | null
          minted_at: string | null
          movement_running: Json | null
          overall_score: number | null
          recommendation: string | null
          status: string | null
        }
        Insert: {
          bezel_condition?: Json | null
          blockchain_mint_tx?: string | null
          bracelet_condition?: Json | null
          case_condition?: Json | null
          caseback_engraving?: Json | null
          created_at?: string | null
          crown_operation?: Json | null
          dial_authenticity?: Json | null
          dial_condition?: Json | null
          hands_authenticity?: Json | null
          id?: string
          inspector_id?: string | null
          inspector_signature_hash?: string | null
          listing_id?: string | null
          lume_response?: Json | null
          minted_at?: string | null
          movement_running?: Json | null
          overall_score?: number | null
          recommendation?: string | null
          status?: string | null
        }
        Update: {
          bezel_condition?: Json | null
          blockchain_mint_tx?: string | null
          bracelet_condition?: Json | null
          case_condition?: Json | null
          caseback_engraving?: Json | null
          created_at?: string | null
          crown_operation?: Json | null
          dial_authenticity?: Json | null
          dial_condition?: Json | null
          hands_authenticity?: Json | null
          id?: string
          inspector_id?: string | null
          inspector_signature_hash?: string | null
          listing_id?: string | null
          lume_response?: Json | null
          minted_at?: string | null
          movement_running?: Json | null
          overall_score?: number | null
          recommendation?: string | null
          status?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "certification_reports_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
        ]
      }
      dealers: {
        Row: {
          created_at: string | null
          email: string | null
          exception_rate_30d: number | null
          id: string
          kyc_status: string | null
          last_active: string | null
          location: Json | null
          name: string
          onboarding_source: string | null
          phone: string | null
          telegram_handle: string | null
          tier: number | null
          trust_score: number | null
          whatsapp_number: string | null
        }
        Insert: {
          created_at?: string | null
          email?: string | null
          exception_rate_30d?: number | null
          id?: string
          kyc_status?: string | null
          last_active?: string | null
          location?: Json | null
          name: string
          onboarding_source?: string | null
          phone?: string | null
          telegram_handle?: string | null
          tier?: number | null
          trust_score?: number | null
          whatsapp_number?: string | null
        }
        Update: {
          created_at?: string | null
          email?: string | null
          exception_rate_30d?: number | null
          id?: string
          kyc_status?: string | null
          last_active?: string | null
          location?: Json | null
          name?: string
          onboarding_source?: string | null
          phone?: string | null
          telegram_handle?: string | null
          tier?: number | null
          trust_score?: number | null
          whatsapp_number?: string | null
        }
        Relationships: []
      }
      exception_records: {
        Row: {
          ai_confidence: number | null
          ai_proposal: Json | null
          corrected_data: Json | null
          created_at: string | null
          events_log: Json | null
          exception_flags: number | null
          exception_payload: Json | null
          extracted_data: Json | null
          id: string
          listing_id: string | null
          resolution_method: string | null
          reviewed_at: string | null
          reviewed_by: string | null
          status: string | null
        }
        Insert: {
          ai_confidence?: number | null
          ai_proposal?: Json | null
          corrected_data?: Json | null
          created_at?: string | null
          events_log?: Json | null
          exception_flags?: number | null
          exception_payload?: Json | null
          extracted_data?: Json | null
          id?: string
          listing_id?: string | null
          resolution_method?: string | null
          reviewed_at?: string | null
          reviewed_by?: string | null
          status?: string | null
        }
        Update: {
          ai_confidence?: number | null
          ai_proposal?: Json | null
          corrected_data?: Json | null
          created_at?: string | null
          events_log?: Json | null
          exception_flags?: number | null
          exception_payload?: Json | null
          extracted_data?: Json | null
          id?: string
          listing_id?: string | null
          resolution_method?: string | null
          reviewed_at?: string | null
          reviewed_by?: string | null
          status?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "exception_records_listing_id_fkey"
            columns: ["listing_id"]
            isOneToOne: false
            referencedRelation: "listings"
            referencedColumns: ["id"]
          },
        ]
      }
      listings: {
        Row: {
          ai_confidence: number | null
          blockchain_passport_id: string | null
          box: boolean | null
          brand: string | null
          case_diameter_mm: number | null
          certification_report_id: string | null
          certification_status: string | null
          condition_score: number | null
          created_at: string | null
          dealer_id: string | null
          dial_color: string | null
          exception_flags: number | null
          extraction_method: string | null
          id: string
          images: Json | null
          inquiry_count: number | null
          material: string | null
          model: string | null
          nickname: string | null
          papers: boolean | null
          price_original_amount: number | null
          price_original_currency: string | null
          price_usd: number | null
          published_at: string | null
          reference: string | null
          source: string | null
          status: string | null
          updated_at: string | null
          view_count: number | null
          year: number | null
        }
        Insert: {
          ai_confidence?: number | null
          blockchain_passport_id?: string | null
          box?: boolean | null
          brand?: string | null
          case_diameter_mm?: number | null
          certification_report_id?: string | null
          certification_status?: string | null
          condition_score?: number | null
          created_at?: string | null
          dealer_id?: string | null
          dial_color?: string | null
          exception_flags?: number | null
          extraction_method?: string | null
          id?: string
          images?: Json | null
          inquiry_count?: number | null
          material?: string | null
          model?: string | null
          nickname?: string | null
          papers?: boolean | null
          price_original_amount?: number | null
          price_original_currency?: string | null
          price_usd?: number | null
          published_at?: string | null
          reference?: string | null
          source?: string | null
          status?: string | null
          updated_at?: string | null
          view_count?: number | null
          year?: number | null
        }
        Update: {
          ai_confidence?: number | null
          blockchain_passport_id?: string | null
          box?: boolean | null
          brand?: string | null
          case_diameter_mm?: number | null
          certification_report_id?: string | null
          certification_status?: string | null
          condition_score?: number | null
          created_at?: string | null
          dealer_id?: string | null
          dial_color?: string | null
          exception_flags?: number | null
          extraction_method?: string | null
          id?: string
          images?: Json | null
          inquiry_count?: number | null
          material?: string | null
          model?: string | null
          nickname?: string | null
          papers?: boolean | null
          price_original_amount?: number | null
          price_original_currency?: string | null
          price_usd?: number | null
          published_at?: string | null
          reference?: string | null
          source?: string | null
          status?: string | null
          updated_at?: string | null
          view_count?: number | null
          year?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "listings_dealer_id_fkey"
            columns: ["dealer_id"]
            isOneToOne: false
            referencedRelation: "dealers"
            referencedColumns: ["id"]
          },
        ]
      }
      master_catalog: {
        Row: {
          brand: string | null
          created_at: string | null
          dial_color: string | null
          id: string
          is_never_collapse: boolean | null
          known_variants: Json | null
          model: string | null
          nickname: string | null
          production_years: Json | null
          reference: string | null
        }
        Insert: {
          brand?: string | null
          created_at?: string | null
          dial_color?: string | null
          id?: string
          is_never_collapse?: boolean | null
          known_variants?: Json | null
          model?: string | null
          nickname?: string | null
          production_years?: Json | null
          reference?: string | null
        }
        Update: {
          brand?: string | null
          created_at?: string | null
          dial_color?: string | null
          id?: string
          is_never_collapse?: boolean | null
          known_variants?: Json | null
          model?: string | null
          nickname?: string | null
          production_years?: Json | null
          reference?: string | null
        }
        Relationships: []
      }
      price_history: {
        Row: {
          box_papers: boolean | null
          brand: string | null
          condition_score: number | null
          created_at: string | null
          dial_color: string | null
          id: string
          liquidity_score: number | null
          price_usd: number | null
          reference: string | null
          source: string | null
          transaction_date: string | null
        }
        Insert: {
          box_papers?: boolean | null
          brand?: string | null
          condition_score?: number | null
          created_at?: string | null
          dial_color?: string | null
          id?: string
          liquidity_score?: number | null
          price_usd?: number | null
          reference?: string | null
          source?: string | null
          transaction_date?: string | null
        }
        Update: {
          box_papers?: boolean | null
          brand?: string | null
          condition_score?: number | null
          created_at?: string | null
          dial_color?: string | null
          id?: string
          liquidity_score?: number | null
          price_usd?: number | null
          reference?: string | null
          source?: string | null
          transaction_date?: string | null
        }
        Relationships: []
      }
      training_examples: {
        Row: {
          accuracy_score: number | null
          ai_output: Json | null
          created_at: string | null
          human_override: Json | null
          id: string
          input_type: string | null
          model_version: string | null
          raw_input: string | null
          used_in_training: boolean | null
        }
        Insert: {
          accuracy_score?: number | null
          ai_output?: Json | null
          created_at?: string | null
          human_override?: Json | null
          id?: string
          input_type?: string | null
          model_version?: string | null
          raw_input?: string | null
          used_in_training?: boolean | null
        }
        Update: {
          accuracy_score?: number | null
          ai_output?: Json | null
          created_at?: string | null
          human_override?: Json | null
          id?: string
          input_type?: string | null
          model_version?: string | null
          raw_input?: string | null
          used_in_training?: boolean | null
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
