package core

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/memodb-io/memobase/src/client/memobase-go/blob"
	"github.com/memodb-io/memobase/src/client/memobase-go/network"
)

type User struct {
	UserID        string
	ProjectClient *MemoBaseClient
	Fields        map[string]interface{}
}

type UserProfile struct {
	ID         string        `json:"id"`
	UpdatedAt  blob.JSONTime `json:"updated_at"`
	CreatedAt  blob.JSONTime `json:"created_at"`
	Content    string        `json:"content"`
	Attributes struct {
		Topic    string `json:"topic"`
		SubTopic string `json:"sub_topic"`
	} `json:"attributes"`
}

func (u *User) Insert(blob blob.BlobInterface) (string, error) {
	reqData := map[string]interface{}{
		"blob_type": blob.GetType(),
		"blob_data": blob.GetBlobData(),
		"fields":    blob.GetFields(),
	}
	if blob.GetCreatedAt() != nil {
		reqData["created_at"] = blob.GetCreatedAt()
	}

	jsonData, err := json.Marshal(reqData)
	if err != nil {
		return "", err
	}

	resp, err := u.ProjectClient.HTTPClient.Post(
		fmt.Sprintf("%s/blobs/insert/%s", u.ProjectClient.BaseURL, u.UserID),
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return "", err
	}

	return baseResp.Data["id"].(string), nil
}

func (u *User) Get(blobID string) (blob.BlobInterface, error) {
	resp, err := u.ProjectClient.HTTPClient.Get(
		fmt.Sprintf("%s/blobs/%s/%s", u.ProjectClient.BaseURL, u.UserID, blobID),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return nil, err
	}

	var blobData blob.BlobData
	jsonData, err := json.Marshal(baseResp.Data)
	if err != nil {
		return nil, err
	}

	if err := json.Unmarshal(jsonData, &blobData); err != nil {
		return nil, err
	}

	return blobData.ToBlob()
}

func (u *User) GetAll(blobType blob.BlobType, page int, pageSize int) ([]string, error) {
	resp, err := u.ProjectClient.HTTPClient.Get(
		fmt.Sprintf("%s/users/blobs/%s/%s?page=%d&page_size=%d",
			u.ProjectClient.BaseURL, u.UserID, blobType, page, pageSize),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return nil, err
	}

	// Handle the response data structure correctly
	data, ok := baseResp.Data["ids"].([]interface{})
	if !ok {
		return nil, fmt.Errorf("unexpected response format for blob IDs")
	}

	// Convert []interface{} to []string
	ids := make([]string, len(data))
	for i, v := range data {
		if str, ok := v.(string); ok {
			ids[i] = str
		} else {
			return nil, fmt.Errorf("unexpected ID type at index %d", i)
		}
	}

	return ids, nil
}

func (u *User) Delete(blobID string) error {
	req, err := http.NewRequest(
		http.MethodDelete,
		fmt.Sprintf("%s/blobs/%s/%s", u.ProjectClient.BaseURL, u.UserID, blobID),
		nil,
	)
	if err != nil {
		return err
	}

	resp, err := u.ProjectClient.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

func (u *User) Flush(blobType blob.BlobType) error {
	resp, err := u.ProjectClient.HTTPClient.Post(
		fmt.Sprintf("%s/users/buffer/%s/%s", u.ProjectClient.BaseURL, u.UserID, blobType),
		"application/json",
		nil,
	)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

func (u *User) Profile() ([]UserProfile, error) {
	resp, err := u.ProjectClient.HTTPClient.Get(
		fmt.Sprintf("%s/users/profile/%s", u.ProjectClient.BaseURL, u.UserID),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return nil, err
	}

	profiles, ok := baseResp.Data["profiles"].([]interface{})
	if !ok {
		return nil, fmt.Errorf("unexpected response format for profiles")
	}

	var result []UserProfile
	for _, p := range profiles {
		profileMap, ok := p.(map[string]interface{})
		if !ok {
			continue
		}

		var profile UserProfile
		jsonData, err := json.Marshal(profileMap)
		if err != nil {
			continue
		}

		if err := json.Unmarshal(jsonData, &profile); err != nil {
			fmt.Printf("Error unmarshaling profile: %v\nData: %s\n", err, jsonData)
			continue
		}

		result = append(result, profile)
	}

	return result, nil
}

func (u *User) UpdateProfile(profileID string, content string, topic string, subTopic string) error {
	reqData := map[string]interface{}{
		"content": content,
		"attributes": map[string]interface{}{
			"topic":     topic,
			"sub_topic": subTopic,
		},
	}

	jsonData, err := json.Marshal(reqData)
	if err != nil {
		return err
	}

	req, err := http.NewRequest(
		http.MethodPut,
		fmt.Sprintf("%s/users/profile/%s/%s", u.ProjectClient.BaseURL, u.UserID, profileID),
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := u.ProjectClient.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

func (u *User) DeleteProfile(profileID string) error {
	req, err := http.NewRequest(
		http.MethodDelete,
		fmt.Sprintf("%s/users/profile/%s/%s", u.ProjectClient.BaseURL, u.UserID, profileID),
		nil,
	)
	if err != nil {
		return err
	}

	resp, err := u.ProjectClient.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

type EventTag struct {
	Tag   string `json:"tag"`
	Value string `json:"value"`
}

type ProfileDelta struct {
	Content    string                 `json:"content"`
	Attributes map[string]interface{} `json:"attributes"`
}

type EventData struct {
	ProfileDelta []ProfileDelta `json:"profile_delta"`
	EventTip     string         `json:"event_tip,omitempty"`
	EventTags    []EventTag     `json:"event_tags,omitempty"`
}

type UserEventData struct {
	ID        string        `json:"id"`
	EventData EventData     `json:"event_data"`
	CreatedAt blob.JSONTime `json:"created_at"`
	UpdatedAt blob.JSONTime `json:"updated_at"`
}

func (u *User) Event(topk int) ([]UserEventData, error) {
	if topk <= 0 {
		topk = 10 // Default value
	}

	resp, err := u.ProjectClient.HTTPClient.Get(
		fmt.Sprintf("%s/users/event/%s?topk=%d", u.ProjectClient.BaseURL, u.UserID, topk),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return nil, err
	}

	events, ok := baseResp.Data["events"].([]interface{})
	if !ok {
		return nil, fmt.Errorf("unexpected response format for events")
	}

	var result []UserEventData
	for _, e := range events {
		eventMap, ok := e.(map[string]interface{})
		if !ok {
			continue
		}

		var event UserEventData
		jsonData, err := json.Marshal(eventMap)
		if err != nil {
			continue
		}

		if err := json.Unmarshal(jsonData, &event); err != nil {
			fmt.Printf("Error unmarshaling event: %v\nData: %s\n", err, jsonData)
			continue
		}

		result = append(result, event)
	}

	return result, nil
}

func (u *User) DeleteEvent(eventID string) error {
	req, err := http.NewRequest(
		http.MethodDelete,
		fmt.Sprintf("%s/users/event/%s/%s", u.ProjectClient.BaseURL, u.UserID, eventID),
		nil,
	)
	if err != nil {
		return err
	}

	resp, err := u.ProjectClient.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

func (u *User) UpdateEvent(eventID string, eventData map[string]interface{}) error {
	jsonData, err := json.Marshal(eventData)
	if err != nil {
		return err
	}

	req, err := http.NewRequest(
		http.MethodPut,
		fmt.Sprintf("%s/users/event/%s/%s", u.ProjectClient.BaseURL, u.UserID, eventID),
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := u.ProjectClient.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	_, err = network.UnpackResponse(resp)
	return err
}

// ContextOptions contains all the optional parameters for the Context method
type ContextOptions struct {
	MaxTokenSize        int            `json:"max_token_size,omitempty"`
	PreferTopics        []string       `json:"prefer_topics,omitempty"`
	OnlyTopics          []string       `json:"only_topics,omitempty"`
	MaxSubtopicSize     *int           `json:"max_subtopic_size,omitempty"`
	TopicLimits         map[string]int `json:"topic_limits,omitempty"`
	ProfileEventRatio   *float64       `json:"profile_event_ratio,omitempty"`
	RequireEventSummary *bool          `json:"require_event_summary,omitempty"`
}

// Context retrieves the user context based on the provided options
func (u *User) Context(options *ContextOptions) (string, error) {
	if options == nil {
		options = &ContextOptions{
			MaxTokenSize: 1000,
		}
	}

	// Build query parameters
	maxTokenSize := 1000
	if options.MaxTokenSize > 0 {
		maxTokenSize = options.MaxTokenSize
	}

	url := fmt.Sprintf("%s/users/context/%s?max_token_size=%d",
		u.ProjectClient.BaseURL, u.UserID, maxTokenSize)

	// Add prefer_topics if provided
	for _, topic := range options.PreferTopics {
		url += fmt.Sprintf("&prefer_topics=%s", topic)
	}

	// Add only_topics if provided
	for _, topic := range options.OnlyTopics {
		url += fmt.Sprintf("&only_topics=%s", topic)
	}

	// Add max_subtopic_size if provided
	if options.MaxSubtopicSize != nil {
		url += fmt.Sprintf("&max_subtopic_size=%d", *options.MaxSubtopicSize)
	}

	// Add topic_limits if provided
	if len(options.TopicLimits) > 0 {
		topicLimitsJSON, err := json.Marshal(options.TopicLimits)
		if err != nil {
			return "", err
		}
		url += fmt.Sprintf("&topic_limits_json=%s", string(topicLimitsJSON))
	}

	// Add profile_event_ratio if provided
	if options.ProfileEventRatio != nil {
		url += fmt.Sprintf("&profile_event_ratio=%f", *options.ProfileEventRatio)
	}

	// Add require_event_summary if provided
	if options.RequireEventSummary != nil {
		requireEventSummary := "false"
		if *options.RequireEventSummary {
			requireEventSummary = "true"
		}
		url += fmt.Sprintf("&require_event_summary=%s", requireEventSummary)
	}

	// Make the request
	resp, err := u.ProjectClient.HTTPClient.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	baseResp, err := network.UnpackResponse(resp)
	if err != nil {
		return "", err
	}

	contextStr, ok := baseResp.Data["context"].(string)
	if !ok {
		return "", fmt.Errorf("unexpected response format for context")
	}

	return contextStr, nil
}
